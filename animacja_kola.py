import pygame
import numpy as np
import imageio
import os
import tempfile

# Inicjalizacja Pygame
pygame.init()

# Stałe
INITIAL_DIAMETER_MM = 5
MAX_DIAMETER_MM = 100
STEP_MM = 1
FRAME_DURATION_MS = 500

# Konwersja mm do pikseli
MM_TO_PIXEL = 2

# Obliczenie liczby kroków
steps = (MAX_DIAMETER_MM - INITIAL_DIAMETER_MM) // STEP_MM + 1
diameters_mm = [INITIAL_DIAMETER_MM + i * STEP_MM for i in range(steps)]
diameters_pixels = [d * MM_TO_PIXEL for d in diameters_mm]

# Ustawienia okna
WIDTH, HEIGHT = 600, 600

# Kolory
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def generate_animation_frames(output_folder="frames"):
    """Generuje klatki animacji i zapisuje jako PNG"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Tworzymy powierzchnię off-screen - UWAGA: pygame.SRCALPHA (z R)
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    frame_files = []
    
    for i, diameter_px in enumerate(diameters_pixels):
        surface.fill(WHITE)
        
        # Rysowanie koła
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        radius = diameter_px // 2
        pygame.draw.circle(surface, RED, (center_x, center_y), radius)
        pygame.draw.circle(surface, BLACK, (center_x, center_y), radius, 2)
        
        # Informacje tekstowe
       
        font = pygame.font.SysFont(None, 36)
        diameter_mm = diameter_px / MM_TO_PIXEL
        info_text = f"Średnica: {diameter_mm:.1f} mm"
        info_surface = font.render(info_text, True, BLACK)
        surface.blit(info_surface, (WIDTH // 2 - info_surface.get_width() // 2, 50))
        
        # Zapisz klatkę
        frame_path = os.path.join(output_folder, f"frame_{i:03d}.png")
        pygame.image.save(surface, frame_path)
        frame_files.append(frame_path)
        
        print(f"Wygenerowano klatkę {i+1}/{len(diameters_pixels)}")
    
    return frame_files

def create_video_from_frames(frame_files, output_video="animacja_kola.mp4", fps=2):
    """Tworzy film z klatek"""
    print("Tworzenie filmu...")
    
    with imageio.get_writer(output_video, fps=fps) as writer:
        for frame_file in frame_files:
            image = imageio.imread(frame_file)
            writer.append_data(image)
            print(f"Dodano klatkę: {frame_file}")
    
    print(f"Film zapisano jako: {output_video}")
    return output_video

def create_multiple_speed_videos():
    """Tworzy filmy z różnymi prędkościami"""
    # Najpierw generujemy klatki
    print("Generowanie klatek animacji...")
    frame_files = generate_animation_frames()
    
    # Tworzymy różne wersje prędkości
    speeds = [
        ("wolno", 1),      # 1 klatka na sekundę
        ("srednio", 5),    # 5 klatek na sekundę
        ("szybko", 10),    # 10 klatek na sekundę
        ("wybuch", 240),   # 240 klatek na sekundę (efekt wybuchu)
    ]
    
    video_files = []
    
    for name, fps in speeds:
        output_file = f"animacja_{name}.mp4"
        create_video_from_frames(frame_files, output_file, fps)
        video_files.append((name, output_file, fps))
    
    return video_files

if __name__ == "__main__":
    # Uruchom generowanie filmów
    videos = create_multiple_speed_videos()
    
    print("\nWygenerowane pliki wideo:")
    for name, filename, fps in videos:
        print(f"  - {filename} ({fps} FPS, tryb: {name})")
    
    print("\nTeraz wstaw te pliki do swojego dokumentu LaTeX używając pakietu 'media9' lub 'movie15'.")
    
    # DODAJ TĘ LINIĘ, ABY OKNO SIĘ NIE ZAMYKAŁO
    input("\nNaciśnij Enter, aby zakończyć...")