__author__ = "hugo.inzirillo"

from napoleontoolbox.dataloader import DataLoader, Provider


def test(ressource: type):
    if issubclass(ressource, Provider):
        print("Provider")
        return ressource()
    elif issubclass(ressource, Provider):
        print("Service")
        return ressource()

if __name__ == '__main__':
    data = DataLoader()


    end = True
