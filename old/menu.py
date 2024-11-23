import readchar
   

def main():
    listopt = ["option 1", "option 2", "option 3", "option 4", "option 5"]
    cursor = 0
    
    keys(listopt, cursor)
            

def display_menu(listopt, cursor):
    for i, op in enumerate(listopt):
        if i == cursor:
            print(f"> {op}") 
        else:
            print(f"  {op}")
def keys(listopt, cursor):
        while True:
            print("\n" * 50)
            display_menu(listopt, cursor)
            key = readchar.readkey() 
            if key == 'q':
                break        
            elif key == 'w': 
                cursor = (cursor - 1) % len(listopt)
            elif key == 's':
                cursor = (cursor + 1) % len(listopt) 
            elif key == '\r':
                umova(listopt, cursor)
                break

def umova(listopt, cursor):       
    if listopt[cursor] == "option 2":
        listopt = ["option 6", "option 7", "option 8", "option 9", "option 10"]
        cursor = 0
        keys(listopt, cursor)
        print("Hello")
        
        input()

    print(f"\nВи вибрали: {listopt[cursor]}")
            
            

if __name__ == "__main__":
    main()