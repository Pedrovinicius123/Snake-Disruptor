#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include <unistd.h>
#include <string.h>
#include <time.h>

int** remove_item(int** array, int size, int index_to_remove) {
    if (index_to_remove < 0 || index_to_remove >= size) {
        return array; // Invalid index, return original
    }

    int** new_array = malloc((size - 1) * sizeof(int*));
    if (!new_array) {
      printf("!!!\n");
      return NULL; // Allocation failed
    }

    for (int i = 0; i < index_to_remove; i++) {
      new_array[i] = malloc(2 * sizeof(int));
      memcpy(new_array[i], array[i], 2 * sizeof(int));
    }

    printf("ERROR?\n");
    free(array); // Free the old array
    printf("ERROR!\n");
    return new_array;
}

int** forward_snake(int** snake, int** available_pos, int* next_pos, int snake_size, int n_positions){
  int last_index = snake_size - 1;
  for (int i = 0; i < last_index; i++){
    snake[i] = snake[i+1];
  }

  for (int k = 0; k < n_positions; k++){
    int* position = (int*) available_pos[k];
    if (next_pos[0] == position[0] && next_pos[1] == position[1]){
      available_pos[k] = snake[last_index]; 
      break;

    }

  }
  
  snake[last_index][0] = next_pos[0];
  snake[last_index][1] = next_pos[1];
  return snake;
  
}

int** grow_snake(int** snake, int** available_pos, int* next_pos, int snake_size, int n_positions){
    printf("???\n");
    snake = realloc(snake, (snake_size + 1) * sizeof(int*));
    printf("!!!\n");
    
    for (int i = 0; i < snake_size-1; i++){
      snake[i] = snake[i+1];
      
    }

    bool break_all = false;

    for (int j = 0; j < snake_size; j++){
      for (int k = 0; k < n_positions; k++){
        int* position = (int*) available_pos[k];
        if (next_pos[0] == position[0] && next_pos[1] == position[1]){
          available_pos = remove_item(available_pos, n_positions, k);
          break_all = true;
          break;

        }

      }

      if (break_all){
        break;

      }
    }
    
}

bool check_position_in(int* current_pos, int** snake, int snake_size){
  for (int i = 0; i < snake_size; i++){
    if (current_pos[0] == snake[i][0] && current_pos[1] == snake[i][1]){
      return true;
          
    }

  }

  return false;

}

bool check_position_out_of_board(int* current_pos, int board_size){
  if (!(0 <= current_pos[0] < board_size) || !(0 <= current_pos[1] < board_size)){
    return true;
  } return false;

}

char set_direction(char current_direction, int snake_size, int* current_pos, int* fruit_pos, int** snake, char* chosed);
char change_direction(char current_direction, int snake_size, int* current_pos, int* next, int* fruit_pos, int** snake, char* chosed) {
    if (!check_position_in(next, snake, snake_size) && !check_position_out_of_board(next, 10)) {
      if (current_direction == 'N' || current_direction == 'S'){
        if (current_pos[1] < fruit_pos[1]) {
            return 'E';
        } else if (current_pos[1] > fruit_pos[1]){
            return 'W';
        } else{
          return current_direction;;
        }
      }

      else if (current_direction == 'E' || current_direction == 'W'){
        if (current_pos[0] < fruit_pos[0]){
          return 'N';

        } else if(current_pos[0] > fruit_pos[0]){
          return 'S';

        } else{
          return current_direction;
        }
      }
    } else {
        bool found = false;
        char chosing, exc;
        int chosed_size = strlen(chosed); // Assuming chosed is null-terminated
        
        switch(current_direction){
          case('N'):
            exc = 'S';
            break;
          
          case('S'):
            exc = 'N';
            break;
          
          case('E'):
            exc = 'W';
            break;

          case('W'):
            exc = 'E';
            break;

        }

        for (int i = 0; i < chosed_size; i++) {
          if (!(current_direction == chosed[i]) && chosed[i] != exc){
            found = true;
            chosing = chosed[i];
            break;
          }
        }

        if (found) {
          char* new_chosed = realloc(chosed, chosed_size + 1 + 1); // +1 for new char, +1 for null terminator
          if (!new_chosed) {
              // Handle memory allocation failure
              return current_direction;
          }
          new_chosed[chosed_size] = chosing;
          new_chosed[chosed_size + 1] = '\0';
          return set_direction(current_direction, snake_size, current_pos, fruit_pos, snake, new_chosed);
        } else {
          return current_direction;
        }
    }
}

char set_direction(char current_direction, int snake_size, int* current_pos, int* fruit_pos, int** snake, char* chosed) {
    int next[2];
    if (current_direction == 'N') {
        next[0] = current_pos[0] - 1; // Fixed: North should decrease row
        next[1] = current_pos[1];
    } else if (current_direction == 'S') {
        next[0] = current_pos[0] + 1; // Fixed: South should increase row
        next[1] = current_pos[1];
    } else if (current_direction == 'E') {
        next[0] = current_pos[0];
        next[1] = current_pos[1] + 1;
    } else if (current_direction == 'W') {
        next[0] = current_pos[0];
        next[1] = current_pos[1] - 1; // Fixed: West should decrease column
    }

    return change_direction(current_direction, snake_size, current_pos, next, fruit_pos, snake, chosed);
}

int** generate_available_positions(int board_size){
  int** available = malloc(board_size * board_size * sizeof(int*));
  for (int i = 0; i < board_size; i++) {
      for (int j = 0; j < board_size; j++) {
          int index = i * board_size + j;
          available[index] = malloc(2 * sizeof(int));
          available[index][0] = i;
          available[index][1] = j;
    }
  }

  return available;

}

void board_print(int** snake, int* fruit, int board_width, int snake_size){
  for (int i = 0; i < board_width; i++){
    for(int j = 0; j < board_width; j++){
      int* pos = malloc(2 * sizeof(int));
      int snake_printed = 0;
      
      pos[0] = i;
      pos[1] = j;
      
      for (int k = 0; k < snake_size; k++){
        if (pos[0] == snake[k][0] && pos[1] == snake[k][1]){
          snake_printed = 1;
          if (k == 0){
            printf(" O ");
            
          } else {
            printf(" o ");
            
          }
          
        }
        
      }
      
      if (pos[0] == fruit[0] && pos[1] == fruit[1]){
        printf(" * ");
        
      } else if (!snake_printed){
        printf(" . ");
        
      }
      
    }
    
    printf("\n");
    
  }
  
}
int main()
{
  srand(time(NULL));
  int* fruit_pos = malloc(2*sizeof(int));
  
  fruit_pos[0] = rand() % 10;
  fruit_pos[1] = rand() % 10;
  
  int snake_start_position[2] = {rand() % 10, rand() % 10};
  int** snake = malloc(sizeof(int*));
  snake[0] = malloc(2 * sizeof(int));
  snake[0] = snake_start_position;
  int snake_size = 1;

  char current_direction = 'N';
  int** available_pos = generate_available_positions(10);
  int available = 100;
  
  while (true) {
    printf("\r");
    int next_pos[2];
    switch(current_direction){
      case('N'):
        next_pos[0] = snake[snake_size-1][0]+1;
        next_pos[1] = snake[snake_size-1][1];
        break;

      case('S'):
        next_pos[0] = snake[snake_size-1][0]-1;
        next_pos[1] = snake[snake_size-1][1];
        break;

      case('E'):
        next_pos[0] = snake[snake_size-1][0];
        next_pos[1] = snake[snake_size-1][1]+1;
        break;

      case('W'):
        next_pos[0] = snake[snake_size-1][0];
        next_pos[1] = snake[snake_size-1][1]-1;
        break;
      
    }
    
    current_direction = set_direction(current_direction, snake_size, snake[0], fruit_pos, snake, "");
    printf("%c\n", current_direction);
    printf("Before error\n");
    printf("%d %d\n", next_pos[0], next_pos[1]);
    if (next_pos[0] == fruit_pos[0] && next_pos[1] == fruit_pos[1]){
      printf("W@!!\n");
      snake = grow_snake(snake, available_pos, next_pos, snake_size, available);
      snake_size++;
      available--;
      fruit_pos = available_pos[rand() % available];

    } else{
      printf("ERROR");
      snake = forward_snake(snake, available_pos, next_pos, snake_size, available);
      
    }  
    
    board_print(snake, fruit_pos, 10, snake_size);
    sleep(1);  // Sleep 300ms so you can see the update
  }
  
  
  printf("Hello, World!");
}