import requests
import json

class ProviderFinder:

    def locales(self):
        return {
            'Argentina': 'AR',
            'Austria': 'AT',
            'Australia': 'AU',
            'Belgium': 'BE',
            'Brazil': 'BR',
            'Canada': 'CA',
            'Chile': 'CL',
            'Colombia': 'CO',
            'Czech Republic': 'CZ',
            'Denmark': 'DK',
            'Ecuador': 'EC',
            'Estonia': 'EE',
            'Finland': 'FI',
            'France': 'FR',
            'Germany': 'DE',
            'Greece': 'GR',
            'Hungary': 'HU',
            'India': 'IN',
            'Indonesia': 'ID',
            'Ireland': 'IE',
            'Italy': 'IT',
            'Japan': 'JA',
            'Latvia': 'LV',
            'Lithuania': 'LT',
            'Malaysia': 'MY',
            'Mexico': 'ME',
            'Netherlands': 'NL',
            'New Zealand': 'NZ',
            'Norway': 'NO',
            'Peru': 'PE',
            'Philippines': 'PH',
            'Poland': 'PL',
            'Portugal': 'PT',
            'Romania': 'RO',
            'Russia': 'RU',
            'Singapore': 'SG',
            'South Africa': 'ZA',
            'South Korea': 'KR',
            'Spain': 'ES',
            'Sweden': 'SE',
            'Switzerland': 'CH',
            'Thailand': 'TH',
            'Turkey': 'TR',
            'United Kingdom': 'GB',
            'United States': 'US',
            'Venezuela': 'VE',
        }

    def languages(self):
        return {
            'English': 'en',
            'Spanish': 'es',
            'German': 'de',
            'French': 'fr',
            'Portugeuse': 'pt',
            'Czech': 'cs',
            'Finnish': 'fi',
            'Greek': 'el',
            'Hungarian': 'hu',
            'Italian': 'it',
            'Japanese': 'jp',
            'Korean': 'ko',
            'Polish': 'pl',
            'Romanian': 'ro',
            'Russian': 'ru',
            'Turkish': 'tr',
        }

    def __get_provider_ids(self, locale):
        provider_data = json.loads(requests.get(f'https://apis.justwatch.com/content/providers/locale/{locale}').text)
        provider_data = {i['id']: i['clear_name'] for i in provider_data}
        return provider_data

    def __get_object_id(self, title, year):
        try:
            object_data = json.loads(requests.get(f'https://apis.justwatch.com/content/urls?include_children=true&path=/au/movie/{title+year}').text)
            return object_data['object_id']
        except:
            try:
                object_data = json.loads(requests.get(f'https://apis.justwatch.com/content/urls?include_children=true&path=/au/movie/{title}').text)
                return object_data['object_id']
            except:
                return 'Error: Title not Found'

    def __fix_input(self, title, year, locale, language):
        title = title.lower().replace(' ', '-')
        year = ('-' + str(year) if year is not None else '')

        if len(locale) != 2:
            try: locale = self.locales()[locale]
            except: locale = 'AU'
        else: locale = locale.upper()

        if len(language) != 2:
            try: language = self.languages()()[language]
            except: language = 'en'
        else: language = language.lower()

        return title, year, language + '_' + locale

    def get_providers(self, title, year=None, locale='AU', language='en'):
        tit, yr, loc = self.__fix_input(title, year, locale, language)
        id = self.__get_object_id(tit, yr)
        if str(id)[:5] == 'Error':
            return id
        
        provider_ids = self.__get_provider_ids(loc)

        jw_data = json.loads(requests.get(f'https://apis.justwatch.com/content/titles/movie/{id}/locale/{loc}').text)
        movie_info = {}
        for i in ['title', 'original_release_year', 'cinema_release_date', 'localized_release_date', 'age_certification', 'runtime', 'external_ids']:
            try: movie_info[i] = jw_data[i]
            except: continue

        providers = []
        for i in jw_data['offers']:
            try:
                service = provider_ids[i['provider_id']]
                url = i['urls']['standard_web']
                quality = i['presentation_type']
                p = {'service': service, 'url': url, 'quality': quality}
                if i['monetization_type'] == 'flatrate': 
                    p['type'] = 'subscription'
                else:
                    p['type'] = i['monetization_type']
                    try:
                        p['retail_price'] = i['retail_price']
                        p['currency'] = i['currency']
                    except: continue
                providers.append(p)
            except: print(i)
        
        return {'movie_info': movie_info, 'providers': providers}
                