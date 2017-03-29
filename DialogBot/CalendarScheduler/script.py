import http.client, urllib.request, urllib.parse, urllib.error, base64, json, re, sys, binascii, codecs
FACE_ID = 'd609c171-8315-4b6e-8d11-e2a24c5a2a6f'
FILE_NAME = 'exicute.txt'
WORDS = [
    'Берендак',
    'jinnin',
    'flyagka',
    'эвент',
    'мероприятие',
    'срочно',
    'спорт',
    'сбор',
    'получение',
    'первокурсник',
    'Староста',
    'деканат',
    'стипендия',
    'внимание',
    'msp',
]
PUBLICS_ID = [
    'overhear_mai',
    'priznavashkifm',
    'skmai',
    'nirs_mai',
    'mai_club',
    'mai_niu',
    'it_world_everyone'

]
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'e33521d5e8da46b2b2492a694875ff4d',
}

f = open(FILE_NAME, 'w', encoding='utf-8')
with f:
    f.write('Hi, Nastya!    ')

f.close()

def get_face_id(url):
    params = urllib.parse.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
    })

    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/detect?%s" % params, '{"url": "%s"}' % url, headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        conn.close()
        if len(json.loads(data)):
            return json.loads(data)[0].get('faceId')
        else:
            return -1
    finally:
        pass


def is_same(face_id_1, face_id_2):
    params = urllib.parse.urlencode({
    })
    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/verify?%s" % params, '{"faceId1":"%s","faceId2":"%s",}' % (face_id_1, face_id_2), headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        conn.close()
        return json.loads(data).get('isIdentical')
    finally:
        pass


def fuzzyfinder(user_input, collection):
    suggestions = []
    pattern = '.*'.join(user_input)
    regex = re.compile(pattern)
    for item in collection:
        match = regex.search(item)
        if match:
            suggestions.append((match.start(), item))
    return [x for _, x in suggestions]


def is_find(text_to_find, big_text):
    return len(fuzzyfinder(text_to_find, [big_text, ])) > 0


def write(data):
    f = open(FILE_NAME, 'a', encoding='utf-8')
    with f:
        f.write(str(data.encode('utf-8')) + "\n")
    exit()


def picturize(url, link='vk.com'):
    return
    if len(url) < 10:
        return
    second_face_id = get_face_id(url)
    if not second_face_id == -1:
        if is_same(FACE_ID, second_face_id):
            write('You was at picture at %s! It is you! %s' % (link, url))
            return


def texturize(text, link='vk.com'):
    for word in WORDS:
        if is_find(word, text):
            write('This is something tou probably wanna hear at public %s%s' % (link, ' '))
            return



def get_posts(public_id, number_of_posts):
    try:
        headers = {
        }

        params = urllib.parse.urlencode({
            'extended': 0,
            'domain': public_id,
            'count': number_of_posts
        })
        conn = http.client.HTTPSConnection('api.vk.com')
        conn.request("GET", "/method/wall.get?%s" % params, headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        conn.close()
        result = json.loads(data).get('response')
        texts = [(result[i+1].get('text')) for i in range(number_of_posts)]
        photos = [(result[i+1].get('attachment').get('photo').get('src')) for i in range(number_of_posts) if result[i+1].get('attachment') is not None and result[i+1].get('attachment').get('photo') is not None]
        for word in texts:
            texturize(word, public_id)
        for photo in photos:
            picturize(photo, public_id)
    finally:
        pass


n = 5
for id in PUBLICS_ID:
    get_posts(id, n)
