class Player:
    def __init__(self, identificator, name, species, stat, image, history, injuries=[], weapons=[["mains nues", "Arme naturelle", "un poing serré peut faire des dégâts.", -3]], armors=[], shells=[], stuff=[], languages=[], capacities=[], notes=[]):
        self.id = identificator
        self.name = name
        self.species = species
        self.history = history
        # stat : [Agilité - 0, Constitution - 1, Force - 2, Précision - 3,  Sens - 4, Social - 5, Survie - 6, Volonté - 7, (XP total, XP économisé) - 8, PV - 9, monnaie de cuivre - 10, couleur - 11]
        self.stat = stat[:]

        if image: self.image = str(image)
        else: self.image = None

        if languages: self.languages = languages[:]
        else: self.languages = ["Commun"]

        self.armors = [Armor(*i) for i in armors]
        self.shells = [Shell(*i) for i in shells]
        self.injuries = [Injury(i) for i in injuries]
        self.weapons = [Weapon(*i) for i in weapons]
        self.stuff = [Stuff(*i) for i in stuff]
        self.capacities = [Capacity(*i) for i in capacities]
        self.notes = notes[:]

    def export(self): return [self.id, self.name, self.species, self.stat, self.image, self.history,[i.export() for i in self.injuries], [i.export() for i in self.weapons], [i.export() for i in self.armors], [i.export() for i in self.shells], [i.export for i in self.stuff], self.languages, [i.export() for i in self.capacities], self.notes]

    def isalive(self): return self.stat[9] > 0

    def natural_healing(self): return (2, 4, 5, 8, 15)[self.stat[1]]

    def max_pv(self): return (10, 16, 20, 24, 30)[self.stat[1]]

    def get_money(self): return self.stat[10] // 100, self.stat[10] % 100 # renvoie (or, cuivre)

    def get_minimum(self, name): return 6 - self.stat[("agilité", "constitution", "force", "précision", "sens", "social", "survie", "volonté").index(name.lower())] # score au dé minimum à obtenir pour valider le lancer

    def add_note(self, note_value):
        self.notes.append([len(self.notes) + 1, note_value])

    def del_note(self, index_target):
        if 0 < index_target <= len(self.notes):
            content = self.notes[index_target - 1][1]
            del(self.notes[index_target - 1])
            for index, value in enumerate(self.notes):
                if index >= index_target - 1: self.notes[index] = [index + 1, value[1]]
            return content
        else:
            return None

    def have_item(self, name):
        for cat_index, category in enumerate((self.weapons, self.armors, self.shells, self.stuff)):
            for index, item in enumerate(category):
                if item.name == name: return (cat_index, category), index

        return None, -1

    def del_item(self, name, category_target=-1):
        category, index = self.have_item(name)
        if index != -1 and (category_target == -1 or (category_target != -1 and category_target == category[0])):
            del(category[1][index])
            return True

        else: return False
    
    def use_stuff(self, stuff_name, nb):
        def get_index(name):
            for index, item in enumerate(self.stuff):
                if item.name == stuff.name: return index

        index = get_index(stuff_name)
        self.stuff[index].nb_use -= nb
        if self.stuff[index].nb_use < -1: self.del_stuff(stuff_name)

    def rest(self):
        pass


class Weapon:
    def __init__(self, name, category, description, bonus):
        self.name = name
        self.category = category
        self.description = description
        self.bonus = bonus

    def export(self): return [self.name, self.category, self.description, self.bonus]


class Armor:
    def __init__(self, name, category, description, stat):
        self.name = name
        self.category = category
        self.description = description
        self.stat = stat

    def export(self): return [self.name, self.category, self.description, self.stat]


class Shell:
    def __init__(self, name, description, shell_points):
        self.name = name
        self.description = description
        self.shell_points = shell_points

    def export(self): return [self.name, self.description, self.shell_points]


class Stuff:
    def __init__(self, name, description, nb_use=-1):
        self.name = name
        self.description = description
        self.nb_use = nb_use

    def export(self): return [self.name, self.description, self.nb_use]


class Injury:
    def __init__(self, description):
        self.description = description

    def export(self): return self.description


class Capacity:
    def __init__(self, name, identificator, ok_to_use):
        self.name = name
        self.id = identificator
        self.ok_to_use = ok_to_use

    def export(self): return [self.name, self.id, self.ok_to_use]

    def isusable(self): return self.ok_to_use