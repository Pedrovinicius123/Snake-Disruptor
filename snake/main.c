#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include <string.h>

double calculate_distance(int* pos1, int*pos2){
  return sqrt(pow(pos1[0] - pos2[0], 2) + pow(pos1[1] - pos2[1], 2));

}

void remove_char(char *str, int index) {
    size_t len = strlen(str);
    if (index >= len) return;
    
    memmove(&str[index], &str[index+1], len - index);
}

void find_and_remove(char *str, char item){
  size_t len = strlen(str);
  for (int i = 0; i < len; i++){
    if (str[i] == item){
      remove_char(str, i);
      break;

    }

  }

}


bool check_position_in(int* current_pos, int** snake, int snake_size){
  for (int i = 0; i < snake_size; i++){
    if (current_pos[0] == snake[i][0] && current_pos[1] == snake[i][1]){
      printf("!!!!\n");
      return true;
          
    }

  }

  return false;

}

bool check_position_out_of_board(int* current_pos, int board_size){
  if (0 > current_pos[0]  || current_pos[0] > board_size || 0 > current_pos[1] || current_pos[1] > board_size){
    return true;
  } return false;

}

char set_direction(char current_direction, int snake_size, int chunk, int* current_pos, int* fruit_pos, int** snake, char* chosed);
char change_direction(char current_direction, int snake_size, int chunk, int* current_pos, int*anterior_pos, int* fruit_pos, int** snake, char* chosed) {
  printf("CURRENT %c\n", current_direction);
  printf("CURRENT position %d %d CURRENT fruit %d %d\n", current_pos[0], current_pos[1], fruit_pos[0], fruit_pos[1]);
  
  if (calculate_distance(current_pos, fruit_pos) > calculate_distance(anterior_pos, fruit_pos)){
    if (current_pos[0] > fruit_pos[0] && (current_direction == 'N' || current_direction == 'S')){
      char result = set_direction('W', snake_size, chunk, current_pos, fruit_pos, snake, chosed);
      return result;

    } else if (current_pos[0] < fruit_pos[0] && (current_direction == 'N' || current_direction == 'S')){
      char result = set_direction('E', snake_size, chunk, current_pos, fruit_pos, snake, chosed);
      return result;

    } else if (current_pos[1] < fruit_pos[1] && (current_direction == 'E' || current_direction == 'W')){
      char result = set_direction('S', snake_size, chunk, current_pos, fruit_pos, snake, chosed);
      return result;

    } else if(current_pos[1] > fruit_pos[1] && (current_direction == 'E' || current_direction == 'W')){
      char result = set_direction('N', snake_size, chunk, current_pos, fruit_pos, snake, chosed);
      return result;

    }
  }

  return set_direction(current_direction, snake_size, chunk, current_pos, fruit_pos, snake, chosed);

}

char set_direction(char current_direction, int snake_size, int chunk, int* current_pos, int* fruit_pos, int** snake, char* chosed) {
    int next[2];
    if (current_direction == 'W') {
        next[0] = current_pos[0] - chunk;
        next[1] = current_pos[1];
    } else if (current_direction == 'E') {
        next[0] = current_pos[0] + chunk;
        next[1] = current_pos[1];
    } else if (current_direction == 'N') {
        next[0] = current_pos[0];
        next[1] = current_pos[1] - chunk;
    } else if (current_direction == 'S') {
        next[0] = current_pos[0];
        next[1] = current_pos[1] + chunk;
    }
    if (!check_position_in(next, snake, snake_size) && !check_position_out_of_board(next, 380)) {
      return current_direction;
    } else{
      
      char* chosed_copy = chosed;
      find_and_remove(chosed_copy, current_direction);

      int chosed_lenght = strlen(chosed_copy);
      printf("CURRENT DIRECTION %c STRLEN %d\n", current_direction, chosed_lenght);
      
      if (chosed_lenght == 0){
        return current_direction;

      }
            
      printf("CHOSED %c\n", chosed[0]);
      for (int i = 0; i < chosed_lenght; i++){
        char result = set_direction(chosed_copy[i], snake_size, chunk, current_pos, fruit_pos, snake, chosed);
        if (result != current_direction){
          return result;
      
        }
        remove_char(chosed, 0);
        
      }

      return chosed_copy[-1%chosed_lenght];
  }
}
