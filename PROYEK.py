#Alvin Tanaya c14210276
#Alfon Pramudita K. C. c14210237
#Otniel Wilson S. c14210293
#Vincentius Actonio C14210213

import random
import tkinter as tk
from tkinter import messagebox

#otniel
def is_solvable(puzzle):
    inversions = 0
    for i in range(puzzle_size * puzzle_size - 1):
        for j in range(i + 1, puzzle_size * puzzle_size):
            if puzzle[j] != empty_cell and puzzle[i] != empty_cell and puzzle[i] > puzzle[j]:
                inversions += 1
    return inversions % 2 == 0

#otniel
def random_puzzle():
    puzzle = list(range(puzzle_size * puzzle_size))
    # print(puzzle)
    random.shuffle(puzzle)
    # print(puzzle, "hasil random")
    if not is_solvable(puzzle):
        puzzle[0], puzzle[1] = puzzle[1], puzzle[0]
        # print(puzzle, "setelah di fix")
    return puzzle

#otniel
# def generate_manually():
#     puzzle =  [0, 1, 8, 6, 7, 4, 5, 3, 2]
#     puzzle = [7, 0, 8, 1, 5, 3, 6, 4, 2]
#     if not is_solvable(puzzle):
#         print("Tidak bisa di solve")
#     return puzzle

#alfon
def get_empty_cell(puzzle):
    return puzzle.index(empty_cell) #dapet index seng kosong

#acto
def get_valid_moves(puzzle):
    empty_cell = get_empty_cell(puzzle)
    # cari row col dari empty cell
    row, col = divmod(empty_cell, puzzle_size)
    valid_moves = []
    if col > 0: #kiri
        valid_moves.append(empty_cell - 1)
    if col < puzzle_size - 1: #kanan
        valid_moves.append(empty_cell + 1)
    if row > 0: #atas
        valid_moves.append(empty_cell - puzzle_size)
    if row < puzzle_size - 1: #bawah
        valid_moves.append(empty_cell + puzzle_size)
    return valid_moves

#alfon
def apply_move(puzzle, move):
    empty_cell = get_empty_cell(puzzle)
    puzzle[empty_cell], puzzle[move] = puzzle[move], puzzle[empty_cell]

#alfon
def is_solved(puzzle):
    return puzzle == list(range(puzzle_size * puzzle_size))

#acto
def heuristic(puzzle):
    distance = 0
    # menghitung distance setiap cell dari curr state dengan goal state.
    for i in range(puzzle_size * puzzle_size):
        if puzzle[i] != empty_cell:
            current_row, current_col = divmod(i, puzzle_size)
            target_row, target_col = divmod(puzzle[i], puzzle_size)
            distance += abs(current_row - target_row) + abs(current_col - target_col)
    return distance


#Alvin
def solve_puzzle(puzzle):
    #memasukkan current puzzle, jumlah move (dimulai dari 0), hasil dari heurictic puzzle dari current puzzle
    open_list = [(puzzle, 0, heuristic(puzzle))]
    closed_list = set()

    while open_list:
        current_puzzle, moves, total_moves_heuristic = min(open_list, key=lambda x: x[1] + x[2]) #ngambil yg paling minimal dari open_list serta jummlah move + nilai heuristic
        open_list.remove((current_puzzle, moves, total_moves_heuristic)) #ngepop dari open list sesuai hasil min
        closed_list.add(tuple(current_puzzle)) #dimasukkan kedalam closed list

        #cek kalau is solved? return jumlah moves
        if is_solved(current_puzzle):
            return moves
        else:
            #kalau tidak, ngambil probabilitas move dari puzzle yang sudah di pop
            valid_moves = get_valid_moves(current_puzzle)
            for move in valid_moves:
                #buat duplicat puzzle dari current puzzle
                duplicat_puzzle = current_puzzle[:]
                #apply probabilitas move
                apply_move(duplicat_puzzle, move)
                #cek apakah duplicat puzzle yang sudah di apply movenya tidak sama dengan di close list (tujuannya tidak kembali ke state sebelumnya)
                if tuple(duplicat_puzzle) not in closed_list :
                    #menambahkan open_list dari duplicat puzzle yang sudah diimplementasikan probabilitas moves yang ada, serta menghitung heuristic dari state yang telah di implementasikan movesnya
                    open_list.append((duplicat_puzzle, moves + 1, heuristic(duplicat_puzzle)))
    return -1


#Alvin
def show_solution_animation(puzzle):
    #nyimpan path index untuk puzzle disolved
    moves = []
    def animation():
        if moves:
            #ngepop 1 per 1 dari array lalu di apply move dan di update
            move = moves.pop(0)
            apply_move(puzzle, move)
            update_puzzle(puzzle)
            #delay animation
            root.after(500, animation)

    #mendapatkan jumlah move
    number_moves = solve_puzzle(puzzle)
    if number_moves > 0:
        messagebox.showinfo(title, f"Puzzle solved in {number_moves} moves!")
        moves = get_solution_moves(puzzle)  #ambil alur jalane dimasukkan ke array
        animation() #mulai animasinya
    else:
        messagebox.showinfo(title, "Puzzle is already solved.")

#vincent
def get_solution_moves(puzzle):
    moves = []
    current_puzzle = puzzle[:]
    while not is_solved(current_puzzle):
        valid_moves = get_valid_moves(current_puzzle)
        for move in valid_moves:
            new_puzzle = current_puzzle[:]
            apply_move(new_puzzle, move)
            if solve_puzzle(new_puzzle) < solve_puzzle(current_puzzle): #nyocokno hasil terbaik dgn state sekarang
                moves.append(move)
                current_puzzle = new_puzzle
                break
    return moves

#Alvin
def remaining(puzzle):
    #mendapatkan jumlah move
    number_moves = solve_puzzle(puzzle)
    if number_moves > 0:
        messagebox.showinfo(title, f"Puzzle solved in {number_moves} moves!")
    else:
        messagebox.showinfo(title, "Puzzle is already solved.")

#vincent
def next_step(puzzle):
    moves = get_solution_moves(puzzle)
    if moves:
        move = moves.pop(0)
        apply_move(puzzle, move)
        update_puzzle(puzzle)
        if is_solved(puzzle):
            messagebox.showinfo(title, "Puzzle solved!")
        else:
            messagebox.showinfo(title, "Next step in the solution.")
    else:
        messagebox.showinfo(title, "Puzzle is already solved.")

#otniel
def shuffle():
    global puzzle, moves

    # dissable buttons saat shuffle (agar tidak ngeleg)
    shuffle_button.config(state=tk.DISABLED)
    hint_next_step_button.config(state=tk.DISABLED)
    hint_remaining_button.config(state=tk.DISABLED)
    solve_button.config(state=tk.DISABLED)

    # puzzle = generate_manually()
    puzzle = random_puzzle()

    # aktifkan kembali buttons
    update_puzzle(puzzle)
    shuffle_button.config(state=tk.NORMAL)
    hint_next_step_button.config(state=tk.NORMAL)
    hint_remaining_button.config(state=tk.NORMAL)
    solve_button.config(state=tk.NORMAL)

#otniel
def update_puzzle(puzzle):
    for i in range(puzzle_size):
        for j in range(puzzle_size):
            value = puzzle[i * puzzle_size + j]
            # print(puzzle[0])
            label = labels[i][j] #index atau posisi pada puzzle grid
            img = image[value]  #ambil image sesuai value
            label.config(image=img, text="", bg="white")
    # print(puzzle)

    if is_solved(puzzle):
        messagebox.showinfo(title, "Puzzle solved!")

#alvin
def click(row, col):
    #nyari index dari tile yang ditekan
    move = row * puzzle_size + col
    #ngecek apakah yang index dari yang ditekan merupakan index yang valid dari probabilitas langkah tile yang kosong
    if move in get_valid_moves(puzzle):
        apply_move(puzzle, move)
        update_puzzle(puzzle)




#ui
title = "8 Puzzle"
width = 470
height = 580
cell_size = 15 #Ukuran kotak dalam(kepingan)
puzzle_size = 3 #Ukuran puzzle, nek 3 ya 3x3
empty_cell = puzzle_size * puzzle_size - 1 #sg mana mau diemptyno

root = tk.Tk() #initiate tkinter
root.title(title) #set judul
root.geometry(f"{width}x{height}") #ukuran basenya
root.resizable(False, False) #ben gaisa ditarik"

image = []
for i in range(puzzle_size * puzzle_size):
    img = tk.PhotoImage(file=r"C:\Users\alfon\OneDrive\Desktop\Kuliah\Proyek\KB_ALA\Puzzle_Aset\{}.png".format(i+1))
    img = img.zoom(cell_size, cell_size)  #ngatur ukuran image dengan kotak cell dngn zoom
    img = img.subsample(25)  #Bantu zoom sisan mengurangi piksel
    image.append(img)#masukno img nang image

#puzzle grid aka buat tempate image
labels = [] #buat array utk nyimpen label"
for i in range(puzzle_size):
    row = [] #buat row nyamping bg sg g paham row wkwk
    for j in range(puzzle_size):
        label = tk.Label(root, text="", width=cell_size * 10, height=cell_size* 10, relief="raised", bg="white") #buat label serta ukurannya
        label.grid(row=i, column=j, padx=1, pady=1) #grid e aka tempate
        label.bind("<Button-1>", lambda e, row=i, col=j: click(row, col)) #idk dbnatu
        row.append(label) #masukno label nang row
    labels.append(row) #masukno row nang labelss

#buttons
shuffle_button = tk.Button(root, text="Shuffle", command=shuffle)
shuffle_button.grid(row=puzzle_size, column=0, padx=5, pady=10)

solve_button = tk.Button(root, text="Solve", command=lambda: show_solution_animation(puzzle))
solve_button.grid(row=puzzle_size, column=1, padx=5, pady=10)

hint_next_step_button = tk.Button(root, text="Hint Next Step", command=lambda: next_step(puzzle))
hint_next_step_button.grid(row=puzzle_size, column=2, padx=5, pady=10)

hint_remaining_button = tk.Button(root, text="Hint Remaining", command=lambda: remaining(puzzle))
hint_remaining_button.grid(row=puzzle_size + 1, column=1, padx=5, pady=15)

#langkah awal puzzle
shuffle()

#Start
root.mainloop()