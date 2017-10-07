# -*- coding: utf-8*-
'''
ESPNNBAParser
2015-11-13: this is all the NFL code rather than NBA code, this is just a skeleton
'''

from bs4 import BeautifulSoup
import logging
import re

class ESPNNBAParser():

    def __init__(self, **kwargs):

        if 'logger' in kwargs:
            logging = kwargs['logger']
        else:
            logging.getLogger(__name__).addHandler(logging.NullHandler())  \
                .addHandler(logging.NullHandler())

    def _parse_row(self, row):
        '''
        '''
        player = {}

        # get the player name / id
        link = row.find("a", {"class": "flexpop"})

        return player

    def espn_player_ids():

        # this is a list of lists
        all_players = {}

        s = EWTScraper()
        page_numbers = list(range(1,11))

        for page_number in page_numbers:
            url = 'http://espn.go.com/nba/salaries/_/page/{0}/seasontype/1'.format(page_number)
            content = s.get(url)
            players = player_page(content)
            for id, name in list(players.items()):
                all_players[id] = name

        with open('espn-nba-players.json', 'w') as outfile:
            json.dump(all_players, outfile, indent=4, sort_keys=True)

        return all_players

    def fivethirtyeight_nba():

        # get player_ids
        with open('/home/sansbacon/PycharmProjects/untitled/espn-nba-players.json', 'r') as infile:
            espn_players = json.load(infile)

        for player_code in list(espn_players.values()):
            player_code = re.sub('[.\']', '', player_code)
            fn = '/home/sansbacon/538/{0}.json'.format(player_code)

            if os.path.isfile(fn):
                print('already have {0}'.format(fn))

            else:
                if len(player_code) > 3:
                    content, from_cache = simscores(player_code)

                    if content:
                        with open(fn, 'w') as outfile:
                            outfile.write(content)
                    else:
                        print('could not get {0}'.format(player_code))

                    if from_cache:
                        print('got url from cache')

                    else:
                        time.sleep(2)

                else:
                    print('could not get {0}'.format(player_code))

    def fix_538player(playerjson):

        # fix keys
        convert = {
         'mp_2015': 'mp_last_season',
         'mp_2016': 'mp_projected',
         'opm_2015': 'opm_last_season',
         'opm_2016': 'opm_projected',
         'per_2015': 'per_last_season',
         'usage': 'usg',
         'value_2015': 'value_last_season',
         'value_2016': 'value_projected',
         'war_mean_2015': 'war_mean_last_season',
         'war_mean_2016': 'war_mean_projected',
        }

        player_stats = playerjson['player_stats']
        player = {convert.get(k, k) : v for k, v in list(player_stats.items())}

        # fix values
        if player['rookie'] == '': player['rookie'] = '0'

        columns = ['age', 'ast_pct', 'ast_pct_ptile_all', 'ast_pct_ptile_pos', 'baseyear', 'blk_pct', 'blk_pct_ptile_all', 'blk_pct_ptile_pos', 'category', 'draft', 'draft_ptile_all', 'draft_ptile_pos', 'ft_freq', 'ft_freq_ptile_all', 'ft_freq_ptile_pos', 'ft_pct', 'ft_pct_ptile_all', 'ft_pct_ptile_pos', 'height', 'height_ptile_all', 'height_ptile_pos', 'mp_last_season', 'mp_projected', 'opm_last_season', 'opm_projected', 'per_last_season', 'player', 'player_id', 'position', 'reb_pct', 'reb_pct_ptile_all', 'reb_pct_ptile_pos', 'rookie', 'stl_pct', 'stl_pct_ptile_all', 'stl_pct_ptile_pos', 'team', 'team_abbr', 'team_short', 'timestamp', 'to_pct', 'to_pct_ptile_all', 'to_pct_ptile_pos', 'tp_freq', 'tp_freq_ptile_all', 'tp_freq_ptile_pos', 'ts_pct', 'ts_pct_ptile_all', 'ts_pct_ptile_pos', 'usg', 'usage_ptile_all', 'usage_ptile_pos', 'value_last_season', 'value_projected', 'war_mean_last_season', 'war_mean_projected', 'weight', 'weight_ptile_all', 'weight_ptile_pos']

        return {col: player[col] for col in columns}


    def player_page(content):

        # <td align="left"><a href="http://espn.go.com/nba/player/_/id/110/kobe-bryant">Kobe Bryant</a>

        players = {}
        soup = BeautifulSoup(content)
        pattern = re.compile('player/_/id/(\d+)/(\w+[^\s]*)', re.IGNORECASE)
        links = soup.findAll('a', href=pattern)

        for link in links:
            match = re.search(pattern, link['href'])

            if match:
                players[match.group(1)] = match.group(2)

            else:
                print('could not get {0}'.format(link['href']))

        return players

    def simscores(player_code):
        s = EWTScraper()
        url = 'http://projects.fivethirtyeight.com/carmelo/{0}.json'.format(player_code)
        content = None
        from_cache = False

        try:
            r = requests.get(url)

            if r.status_code == requests.codes.ok:
                content = r.text
                from_cache = r.from_cache

        except requests.exceptions.RequestException as e:
            print(e)

        return content, from_cache

    _espn_id_playercode = {"1000": "brendan-haywood", "1007": "joe-johnson", "1015": "tony-parker", "1017": "zach-randolph", "1018": "jason-richardson", "1026": "gerald-wallace", "110": "kobe-bryant", "1135": "chris-andersen", "136": "vince-carter", "165": "jamal-crawford", "1705": "caron-butler", "1708": "mike-dunleavy", "1711": "drew-gooden", "1713": "nene-hilario", "1765": "matt-barnes", "1781": "luis-scola", "1966": "lebron-james", "1975": "carmelo-anthony", "1977": "chris-bosh", "1978": "nick-collison", "1981": "kirk-hinrich", "1982": "chris-kaman", "1985": "luke-ridnour", "1987": "dwyane-wade", "1994": "steve-blake", "2011": "kyle-korver", "2016": "zaza-pachulia", "215": "tim-duncan", "2166": "leandro-barbosa", "2167": "boris-diaw", "2177": "david-west", "2178": "mo-williams", "2184": "udonis-haslem", "2309097": "damjan-rudez", "2325975": "chris-johnson", "2327577": "jamychal-green", "2367": "tony-allen", "2382": "devin-harris", "2384": "dwight-howard", "2386": "andre-iguodala", "2389": "al-jefferson", "2394": "kevin-martin", "2419": "anderson-varejao", "2426": "trevor-ariza", "2429": "luol-deng", "2433": "kris-humphries", "2439": "jameer-nelson", "2448": "beno-udrih", "2488651": "ryan-kelly", "2488653": "mason-plumlee", "2488689": "sean-kilpatrick", "2488721": "lamar-patterson", "2488845": "cory-jefferson", "2488945": "tim-frazier", "2488958": "solomon-hill", "2488999": "c.j.-wilcox", "2489530": "troy-daniels", "2489663": "kelly-olynyk", "2489716": "matthew-dellavedova", "2490117": "kyle-casey", "2490149": "c.j.-mccollum", "2490620": "robert-covington", "2527963": "victor-oladipo", "2528210": "tim-hardaway-jr.", "2528353": "tony-snell", "2528354": "cameron-bairstow", "2528386": "joseph-young", "2528447": "ray-mccallum", "2528588": "doug-mcdermott", "2528779": "reggie-bullock", "2530276": "tyler-johnson", "2530334": "deonte-burton", "2530596": "andre-roberson", "2530682": "melvin-ejim", "2530722": "phil-pressey", "2530780": "shabazz-napier", "2531038": "russ-smith", "2531047": "jerian-grant", "2531100": "adreian-payne", "2531186": "corey-hawkins", "2531210": "allen-crabbe", "2531362": "anthony-brown", "2531364": "josh-huestis", "2534781": "gorgui-dieng", "2560823": "zoran-dragic", "2566741": "k.j.-mcdaniels", "2578213": "ben-mclemore", "2578239": "pat-connaughton", "2578259": "darrun-hilliard-ii", "2579258": "cody-zeller", "2579260": "trey-burke", "2579278": "shannon-scott", "2579294": "frank-kaminsky-iii", "2580365": "larry-nance-jr.", "2581018": "kentavious-caldwell-pope", "2581177": "rodney-hood", "2581190": "josh-richardson", "2583639": "elfrid-payton", "2594816": "p.j.-hairston", "2594920": "greg-whittington", "2594922": "otto-porter-jr.", "2595516": "norman-powell", "2596107": "alex-len", "2596108": "michael-carter-williams", "2596110": "rakeem-christmas", "2596158": "shane-larkin", "261": "kevin-garnett", "2614962": "jarnell-stokes", "272": "manu-ginobili", "2745": "brandon-bass", "2747": "andrew-bogut", "2751": "monta-ellis", "2753": "raymond-felton", "2754": "channing-frye", "2758": "marcin-gortat", "2767": "ersan-ilyasova", "2768": "jarrett-jack", "2772": "david-lee", "2774": "ian-mahinmi", "2778": "c.j.-miles", "2779": "chris-paul", "2795": "martell-webster", "2797": "marvin-williams", "2798": "deron-williams", "2799": "louis-williams", "2806": "jose-calderon", "2959745": "sergey-karasev", "2959753": "joffrey-lauvergne", "2968361": "raul-neto", "2968436": "joe-ingles", "2968439": "aron-baynes", "2982334": "t.j.-warren", "2982340": "justin-anderson", "2983": "lamarcus-aldridge", "2983727": "r.j.-hunter", "2987": "andrea-bargnani", "2990992": "marcus-smart", "2991009": "grant-jerrett", "2991039": "glenn-robinson-iii", "2991041": "mitch-mcgary", "2991042": "nik-stauskas", "2991055": "montrezl-harrell", "2991184": "sam-dekker", "2991235": "steven-adams", "2991280": "nerlens-noel", "2991281": "archie-goodwin", "2991282": "willie-cauley-stein", "2991475": "bryce-dejean-jones", "2993370": "richaun-holmes", "2993873": "jordan-adams", "2993874": "kyle-anderson", "2993875": "shabazz-muhammad", "2995706": "mario-hezonja", "2999547": "gary-harris", "3003": "randy-foye", "3005": "rudy-gay", "3008": "ryan-hollins", "3012": "kyle-lowry", "3015": "paul-millsap", "3018": "steve-novak", "3024": "j.j.-redick", "3026": "rajon-rondo", "3028": "thabo-sefolosha", "3032976": "rudy-gobert", "3032977": "giannis-antetokounmpo", "3032979": "dennis-schroder", "3032980": "lucas-nogueira", "3033": "p.j.-tucker", "3033031": "walter-tavares", "3041": "lou-amundson", "3055": "j.j.-barea", "3056600": "jabari-parker", "3059281": "tyler-ennis", "3059318": "joel-embiid", "3059319": "andrew-wiggins", "3064230": "cameron-payne", "3064290": "aaron-gordon", "3064291": "rondae-hollis-jefferson", "3064440": "zach-lavine", "3064447": "delon-wright", "3064482": "bobby-portis", "3064509": "james-young", "3064510": "aaron-harrison", "3064514": "julius-randle", "3064517": "jarell-martin", "3064520": "jordan-mickey", "3074752": "terry-rozier", "3078284": "noah-vonleh", "3102528": "dante-exum", "3102529": "clint-capela", "3102530": "jusuf-nurkic", "3102531": "kristaps-porzingis", "3102534": "damien-inglis", "3112335": "nikola-jokic", "3113297": "bruno-caboclo", "3113587": "cristiano-da-silva-felicio", "3133600": "cliff-alexander", "3133603": "kelly-oubre-jr.", "3133628": "myles-turner", "3134881": "stanley-johnson", "3135046": "tyus-jones", "3135047": "justise-winslow", "3135048": "jahlil-okafor", "3136193": "devin-booker", "3136195": "karl-anthony-towns", "3136196": "trey-lyles", "3136776": "d'angelo-russell", "3137733": "rashad-vaughn", "3153165": "chris-mccullough", "3155535": "kevon-looney", "3187": "arron-afflalo", "3190": "marco-belinelli", "3191": "corey-brewer", "3192": "aaron-brooks", "3194": "wilson-chandler", "3195": "mike-conley", "3201": "jared-dudley", "3202": "kevin-durant", "3206": "marc-gasol", "3209": "jeff-green", "3211": "spencer-hawes", "3213": "al-horford", "3217": "carl-landry", "3220": "josh-mcroberts", "3224": "joakim-noah", "3231": "ramon-sessions", "3232": "jason-smith", "3233": "tiago-splitter", "3235": "rodney-stuckey", "3242": "brandan-wright", "3243": "nick-young", "3244": "thaddeus-young", "3247": "joel-anthony", "3276": "anthony-tolliver", "3277": "c.j.-watson", "3410": "alexis-ajinca", "3412": "ryan-anderson", "3413": "darrell-arthur", "3414": "omer-asik", "3415": "d.j.-augustin", "3416": "nicolas-batum", "3417": "jerryd-bayless", "3419": "mario-chalmers", "3421": "joey-dorsey", "3423": "goran-dragic", "3428": "danilo-gallinari", "3431": "eric-gordon", "3436": "roy-hibbert", "3437": "j.j.-hickson", "3439": "serge-ibaka", "3443": "sasha-kaun", "3444": "kosta-koufos", "3445": "courtney-lee", "3447": "robin-lopez", "3449": "kevin-love", "3452": "javale-mcgee", "3453": "nikola-pekovic", "3456": "derrick-rose", "3457": "brandon-rush", "3460": "marreese-speights", "3462": "jason-thompson", "3464": "henry-walker", "3468": "russell-westbrook", "3474": "anthony-morrow", "3554": "omri-casspi", "3593": "bojan-bogdanovic", "3892818": "emmanuel-mudiay", "3911666": "luis-montero", "3964": "patrick-beverley", "3965": "dejuan-blair", "3970": "demarre-carroll", "3971": "earl-clark", "3973": "darren-collison", "3974": "dante-cunningham", "3975": "stephen-curry", "3978": "demar-derozan", "3981": "wayne-ellington", "3983": "tyreke-evans", "3988": "danny-green", "3989": "blake-griffin", "3991": "tyler-hansbrough", "3992": "james-harden", "3993": "gerald-henderson", "3995": "jrue-holiday", "3996": "lester-hudson", "3997": "brandon-jennings", "3998": "jonas-jerebko", "3999": "james-johnson", "4000": "ty-lawson", "4003": "jodie-meeks", "4004": "patty-mills", "4011": "ricky-rubio", "4015": "jeff-teague", "4023": "garrett-temple", "4158": "jerel-mcneal", "4182": "pablo-prigioni", "4195": "kostas-papanikolaou", "4229": "reggie-williams", "4232": "alonzo-gee", "4237": "john-wall", "4238": "eric-bledsoe", "4239": "evan-turner", "4240": "avery-bradley", "4242": "james-anderson", "4244": "lance-stephenson", "4245": "terrico-white", "4247": "wesley-johnson", "4248": "al-farouq-aminu", "4249": "gordon-hayward", "4250": "luke-babbitt", "4251": "paul-george", "4253": "quincy-pondexter", "4258": "demarcus-cousins", "4259": "ed-davis", "4264": "patrick-patterson", "4267": "cole-aldrich", "4269": "nemanja-bjelica", "4270": "trevor-booker", "4284": "tibor-pleiss", "4291": "greivis-vasquez", "4294": "elliot-williams", "4298": "timofey-mozgov", "4299": "jeremy-lin", "4300": "gary-neal", "4321": "elijah-millsap", "4376": "boban-marjanovic", "4385": "mirza-teletovic", "609": "dirk-nowitzki", "6424": "lavoy-allen", "6425": "keith-benson", "6427": "bismack-biyombo", "6429": "alec-burks", "6430": "jimmy-butler", "6431": "norris-cole", "6433": "kenneth-faried", "6434": "jimmer-fredette", "6436": "jordan-hamilton", "6440": "tobias-harris", "6443": "reggie-jackson", "6446": "cory-joseph", "6447": "enes-kanter", "6450": "kawhi-leonard", "6452": "jon-leuer", "6454": "shelvin-mack", "6459": "nikola-mirotic", "6460": "e'twaun-moore", "6461": "markieff-morris", "6464": "donatas-motiejunas", "6466": "chandler-parsons", "6468": "iman-shumpert", "6469": "kyle-singler", "6472": "isaiah-thomas", "6475": "klay-thompson", "6477": "jonas-valanciunas", "6478": "nikola-vucevic", "6479": "kemba-walker", "6480": "derrick-williams", "6485": "lance-thomas", "6486": "jarrid-famous", "6569": "alan-anderson", "6576": "quincy-acy", "6577": "furkan-aldemir", "6578": "harrison-barnes", "6579": "will-barton", "6580": "bradley-beal", "6581": "jae-crowder", "6583": "anthony-davis", "6585": "andre-drummond", "6587": "festus-ezeli", "6588": "evan-fournier", "6589": "draymond-green", "6591": "maurice-harkless", "6592": "john-henson", "6594": "john-jenkins", "6597": "terrence-jones", "6598": "perry-jones", "6601": "michael-kidd-gilchrist", "6603": "jeremy-lamb", "6605": "meyers-leonard", "6606": "damian-lillard", "6607": "kendall-marshall", "6609": "khris-middleton", "6614": "andrew-nicholson", "6615": "kyle-o'quinn", "6616": "miles-plumlee", "6617": "austin-rivers", "6618": "thomas-robinson", "6619": "terrence-ross", "662": "paul-pierce", "6622": "mike-scott", "6624": "jared-sullinger", "6628": "dion-waiters", "6630": "tony-wroten", "6631": "tyler-zeller", "6635": "chris-copeland", "6637": "kent-bazemore", "6641": "brian-roberts", "984": "tyson-chandler", "996": "pau-gasol"}

if __name__ == "__main__":
    pass
