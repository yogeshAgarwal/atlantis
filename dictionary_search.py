import requests
import json

class DictornaySearch:
    def hit_api(self, word):
        base_url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"
        url = base_url + word
        response = requests.get(url)
        if response.status_code in [200, 201]:
            text_data = response.text
            try:
                data = json.loads(text_data)
                final_string = self.format_data(data)
            except:
                return "Please give correct input, Dictionary doesn't have this letter"
            return final_string
        else:
            return "Please give correct input, Dictionary doesn't have this letter"

    def format_data(self, data):
        final_string = ""
        if type(data) == list:
            data = data[0]
        final_string += data.get('word') + ". "
        final_string += data['meanings'][0]['partOfSpeech'] + ". "
        final_string += data['meanings'][0]['definitions'][0]['definition']
        return final_string




if __name__ == '__main__':
    input_word = input("Word?  ")
    obj = DictornaySearch()
    print(obj.hit_api(input_word))
