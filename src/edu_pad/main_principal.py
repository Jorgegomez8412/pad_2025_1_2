from edu_pad import main_extraccion, main_inges

def main():
    print("Ejecutando extracción...")
    main_extraccion.main()
    
    print("Ejecutando ingestión...")
    main_inges.main()

if __name__ == "__main__":
    main()