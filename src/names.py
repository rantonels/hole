import random

LUTFEM = ['Adara', 'Adena', 'Adrianne', 'Alarice', 'Alvita', 'Amara', 'Ambika', 'Antonia', 'Araceli', 'Balandria', 'Basha',
'Beryl', 'Bryn', 'Callia', 'Caryssa', 'Cassandra', 'Casondrah', 'Chatha', 'Ciara', 'Cynara', 'Cytheria', 'Dabria', 'Darcei',
'Deandra', 'Deirdre', 'Delores', 'Desdomna', 'Devi', 'Dominique', 'Drucilla', 'Duvessa', 'Ebony', 'Fantine', 'Fuscienne',
'Gabi', 'Gallia', 'Hanna', 'Hedda', 'Jerica', 'Jetta', 'Joby', 'Kacila', 'Kagami', 'Kala', 'Kallie', 'Keelia', 'Kerry',
'Kerry-Ann', 'Kimberly', 'Killian', 'Kory', 'Lilith', 'Lucretia', 'Lysha', 'Mercedes', 'Mia', 'Maura', 'Perdita', 'Quella',
'Riona', 'Safiya', 'Salina', 'Severin', 'Sidonia', 'Sirena', 'Solita', 'Tempest', 'Thea', 'Treva', 'Trista', 'Vala', 'Winta']

LUTMAL = ['Abaet', 'Abarden', 'Aboloft', 'Acamen', 'Achard', 'Ackmard', 'Adeen', 'Aerden', 'Afflon', 'Aghon', 'Agnar', 'Ahalfar', 'Ahburn', 'Ahdun', 'Aidan', 'Airen', 'Airis', 'Albright', 'Aldaren', 'Alderman', 'Aldren', 'Alkirk', 'Allso', 'Amerdan', 'Amitel', 'Anfar', 'Anumi', 'Anumil', 'Asden', 'Asdern', 'Asen', 'Aslan', 'Atar', 'Atgur', 'Atlin', 'Auchfor', 'Auden', 'Ault', 'Ayrie', 'Bacohl', 'Badeek', 'Baduk', 'Balati', 'Baradeer', 'Barkydle', 'Basden', 'Bayde', 'Beck', 'Bedic', 'Beeron', 'Bein', 'Beson', 'Besur', 'Besurlde', 'Bewul', 'Biedgar', 'Bildon', 'Biston', 'Bithon', 'Boal', 'Boaldelr', 'Bolrock', 'Brakdern', 'Breanon', 'Bredere', 'Bredin', 'Bredock', 'Breen', 'Brighton', 'Bristan', 'Buchmeid', 'Bue', 'Busma', 'Buthomar', 'Bydern', 'Caelholdt', 'Cainon', 'Calden', 'Camchak', 'Camilde', 'Cardon', 'Casden', 'Cayold', 'Celbahr', 'Celorn', 'Celthric', 'Cemark', 'Cerdern', 'Cespar', 'Cether', 'Cevelt', 'Chamon', 'Chesmarn', 
'Chidak', 'Cibrock', 'Cipyar', 'Ciroc', 'Codern', 'Colthan', 'Connell', 'Cordale', 'Cos', 'Cosdeer', 'Cuparun', 'Cusmirk', 'Cydare', 'Cylmar', 'Cythnar', 'Daburn', 'Daermod', 'Dak', 'Dakamon', 'Dakkone', 'Dalburn', 'Dalmarn', 'Dapvhir', 'Darkboon', 'Darkkon', 'Darko', 'Darkspur', 'Darmor', 'Darpick', 'Dasbeck', 'Dask', 'Deathmar', 'Defearon', 'Derik', 'Derrin', 'Desil', 'Dessfar', 'Dinfar', 'Dismer', 'Doceon', 'Dochrohan', 'Dokoran', 'Dorn', 'Dosoman', 'Drakoe', 'Drakone', 'Drandon', 'Drit', 'Dritz', 'Drophar', 'Dryden', 'Dryn', 'Duba', 'Dukran', 'Duran', 'Durmark', 'Dusaro', 'Dyfar', 'Dyten', 'Eard', 'Eckard', 'Efamar', 'Efar', 'Egmardern', 'Eiridan', 'Ekgamut', 'Eli', 'Elik', 'Elson', 'Elthin', 'Enbane', 'Endor', 'Enidin', 'Enoon', 'Enro', 'Erikarn', 'Erim', 'Eritai', 'Escariet', 'Espardo', 'Etar', 'Etburn', 'Etdar', 'Ethen', 'Etmere', 'Etran', 'Faoturk', 'Faowind', 'Fearlock', 'Fenrirr', 'Fetmar', 'Feturn', 'Ficadon', 'Fickfylo', 'Fildon', 'Firedorn', 'Firiro', 'Floran', 'Folmard', 'Fraderk', 'Fronar', 'Fydar', 'Fyn', 'Gafolern', 'Gai', 'Galain', 'Galiron', 'Gametris', 'Gauthus', 
'Gemardt', 'Gemedern', 'Gemedes', 'Gerirr', 'Geth', 'Gib', 'Gibolock', 'Gibolt', 'Gith', 'Gom', 'Gosford', 'Gothar', 'Gothikar', 'Gresforn', 'Grimie', 'Gryn', 'Gundir', 'Gustov', 'Guthale', 'Gybol', 'Gybrush', 'Halmar', 'Harrenhal', 'Hasten', 'Hectar', 'Hecton', 'Heramon', 'Hermenze', 'Hermuck', 'Hezak', 'Hildale', 'Hildar', 'Hileict', 'Hydale', 'Hyten', 'Iarmod', 'Idon', 'Ieli', 'Ieserk', 'Ikar', 'Ilgenar', 'Illilorn', 'Illium', 'Ingel', 'Ipedorn', 'Irefist', 'Ironmark', 'Isen', 'Isil', 'Ithric', 'Jackson', 'Jalil', 'Jamik', 'Janus', 'Jayco', 'Jaython', 'Jesco', 'Jespar', 'Jethil', 'Jex', 'Jib', 'Jibar', 'Jin', 'Juktar', 'Julthor', 'Jun', 'Justal', 'Kafar', 'Kaldar', 'Kellan', 'Keran', 'Kesad', 'Kesmon', 'Kethren', 'Kib', 'Kibidon', 'Kiden', 'Kilbas', 'Kilburn', 'Kildarien', 'Kimdar', 'Kinorn', 'Kip', 'Kirder', 'Kodof', 'Kolmorn', 'Kyrad', 'Lackus', 'Lacspor', 'Laderic', 'Lafornon', 'Lahorn', 'Laracal', 'Ledale', 'Leit', 'Lephar', 'Lephidiles', 'Lerin', 'Lesphares', 'Letor', 'Lidorn', 'Lin', 'Liphanes', 'Loban', 'Lox', 'Ludokrin', 'Luphildern', 'Lupin', 'Macon', 'Madarlon', 'Mafar', 'Marderdeen', 'Mardin', 'Markard', 'Markdoon', 'Marklin', 'Mashasen', 'Mathar', 'Medarin', 'Medin', 'Mellamo', 'Meowol', 'Merdon', 'Meridan', 'Merkesh', 'Mesah', "Mes'ard", 'Mesophan', 'Mesoton', 'Mezo', 'Michael', 'Mick', 'Mickal', 'Migorn', 'Milo', 'Miphates', "Mi'talrythin", 'Mitar', 'Modric', 'Modum', 'Mudon', 'Mufar', 'Mujarin', 'Mylo', 'Mythik', 'Mythil', 'Nadeer', 'Nalfar', 'Namorn', 'Naphates', 'Neowyld', 'Nidale', 'Nikpal', 'Nikrolin', 'Niktohal', 'Niro', 'Noford', 'Nothar', 'Nuthor', 'Nuwolf', 'Nydale', 
 'Ocarin', 'Occelot', 'Occhi', 'Odaren', 'Odeir', 'Ohethlic', 'Okar', 'Omaniron', 'Omarn', 'Orin', 'Ospar', 'Othelen', 'Oxbaren', 'Padan', 'Palid', 'Papur', 'Peitar', 'Pelphides', 'Pender', 'Pendus', 'Perder', 'Perol', 'Phairdon', 'Phemedes', 'Phexides', 'Phoenix', 'Picon', 'Pictal', 'Picumar', 'Pildoor', 'Pixdale', 'Ponith', 'Poran', 'Poscidion', 'Prothalon', 'Puthor', 'Pyder', 'Qeisan', 'Qidan', 'Quiad', 'Quid', 'Quiss', 'Qupar', "Radag'mal", 'Randar', 'Raysdan', 'Rayth', 'Reaper', 'Resboron', 'Reth', 'Rethik', 'Rhithik', 'Rhithin', 'Rhysling', 'Riandur', 'Rikar', 'Rismak', 'Riss', 'Ritic', 'Rogeir', 'Rogist', 'Rogoth', 'Rophan', 'Rulrindale', 'Rydan', 'Ryfar', 'Ryfar', 'Ryodan', 'Rysdan', 'Rythen', 'Sabal', 'Sadareen', 'Safilix', 'Samon', 'Samot', 'Sasic', 'Scoth', 'Scythe', 'Secor', 'Sed', 'Sedar', 'Senick', 'Senthyril', 'Serin', 'Sermak', 'Seryth', 'Sesmidat', 'Seth', 'Setlo', 'Shade', 'Shadowbane', 'Shane', 'Shard', 'Shardo', 'Shillen', 'Silco', 'Sildo', "Sil'forrin", 'Silpal', 'Sithik', 'Soderman', 'Sothale', 'Staph', 'Stenwulf', 
'Steven', 'Suktor', 'Suth', 'Sutlin', 'Syr', 'Syth', 'Sythril', 'Talberon', 'Telpur', 'Temil', 'Temilfist', 'Tempist', 'Teslanar', 'Tespar', 'Tessino', 'Tethran', 'Thiltran', 'Tholan', 'Tibers', 'Tibolt', 'Ticharol', 'Tilner', 'Tithan', 'Tobale', 'Tolle', 'Tolsar', 'Toma', 'Tothale', 'Tousba', 'Towerlock', 'Tuk', 'Tuscanar', 'Tusdar', 'Uerthe', 'Ugmar', 'Uhrd', 'Undin', 'Updar', 'Uther', 'Vaccon', 'Vacone', 'Valkeri', 'Valynard', 'Vectomon', 'Veldahar', 'Vespar', 'Vethelot', 'Victor', 'Vider', 'Vigoth', 'Vilan', 'Vildar', 'Vinald', 'Vinkolt', 'Virde', 'Voltain', 'Volux', 'Voudim', 'Vythethi', 
 'Walkar', 'Wanar', 'Wekmar', 'Werymn', 'Weshin', 'William', 'Willican', 'Wilte', 'Wiltmar', 'Wishane', 'Witfar', 'Wrathran', 'Wraythe', 'Wuthmon', 'Wyder', 'Wyeth', 'Wyvorn', 'Xander', 'Xavier', 'Xenil', 'Xex', 'Xithyl', 'Xuio', 'Yabaro', 'Yepal', 'Yesirn', 'Yssik', 'Yssit', 'Zak', 'Zakarn', 'Zecane', 'Zidar', 'Zigmal', 'Zile', 'Zotar', 'Zutar', 'Zyten']


###############################################################################
# Markov Name model
# A random name generator, by Peter Corbett
# http://www.pick.ucam.org/~ptc24/mchain.html
# This script is hereby entered into the public domain
###############################################################################
class Mdict:
    def __init__(self):
        self.d = {}
    def __getitem__(self, key):
        if key in self.d:
            return self.d[key]
        else:
            raise KeyError(key)
    def add_key(self, prefix, suffix):
        if prefix in self.d:
            self.d[prefix].append(suffix)
        else:
            self.d[prefix] = [suffix]
    def get_suffix(self,prefix):
        l = self[prefix]
        return random.choice(l)  

class MName:
    """
    A name from a Markov chain
    """
    def __init__(self, TAB, chainlen = 2):
        self.TAB = TAB
        """
        Building the dictionary
        """
        if chainlen > 10 or chainlen < 1:
            print "Chain length must be between 1 and 10, inclusive"
            sys.exit(0)
    
        self.mcd = Mdict()
        oldnames = []
        self.chainlen = chainlen
    
        for l in self.TAB:
            l = l.strip()
            oldnames.append(l)
            s = " " * chainlen + l
            for n in range(0,len(l)):
                self.mcd.add_key(s[n:n+chainlen], s[n+chainlen])
            self.mcd.add_key(s[len(l):len(l)+chainlen], "\n")
    
    def New(self):
        """
        New name from the Markov chain
        """
        prefix = " " * self.chainlen
        name = ""
        suffix = ""
        while True:
            suffix = self.mcd.get_suffix(prefix)
            if suffix == "\n" or len(name) > 9:
                break
            else:
                name = name + suffix
                prefix = prefix[1:] + suffix
        return name.capitalize()  



'''g = MName(LUTFEM,2)
g2 = MName(LUTMAL,2)

for i in range(100):
    print g.New()

print

for i in range(100):
    print g2.New()'''
