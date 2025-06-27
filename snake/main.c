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

double calculate_distance_from_border(char current_direction, int* current_pos){
  if (current_direction == 'N'){
    return 400 - current_pos[1];

  } else if (current_direction == 'S'){
    return current_pos[1];

  } else if (current_direction == 'W'){
    return current_pos[0];

  } else{
    return 400 - current_pos[0];

  }

}

double check_obstacles(char current_direction, int snake_size, int**next_snake, int*current_pos, int* fruit_pos){
  double count = 0;
  for (int i = 1; i < snake_size; i++){
    if (current_direction == 'S'){
      if (current_pos[0] == next_snake[i][0] && current_pos[1] < next_snake[i][1] && fruit_pos[0] == current_pos[0]){
        count += pow(calculate_distance(current_pos, next_snake[i]), 2) * pow(calculate_distance_from_border('S', current_pos), -1);
      }
    }if (current_direction == 'N'){
      if (current_pos[0] == next_snake[i][0] && current_pos[1] > next_snake[i][1] && fruit_pos[0] == current_pos[0]){
        count += pow(calculate_distance(current_pos, next_snake[i]), 2) * pow(calculate_distance_from_border('N', current_pos), -1);
      }
    }if (current_direction == 'W'){
      if (current_pos[1] == next_snake[i][1] && current_pos[0] > next_snake[i][0] && fruit_pos[1] == current_pos[1]){
        count += pow(calculate_distance(current_pos, next_snake[i]), 2) * pow(calculate_distance_from_border('W', current_pos), -1);
      }
    }if (current_direction == 'S'){
      if (current_pos[0] == next_snake[i][1] && current_pos[0] < next_snake[i][0] && fruit_pos[1] == current_pos[1]){
        count += pow(calculate_distance(current_pos, next_snake[i]), 2) * pow(calculate_distance_from_border('E', current_pos), -1);
      }
    }
  }
  return count;
}


bool check_position_in(int* current_pos, int** snake, int snake_size){
  for (int i = 1; i < snake_size; i++){
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

char set_direction(char current_direction, char anterior_direction, int snake_size, int chunk, bool away, int* current_pos, int* fruit_pos, int** snake, int** next_snake, char* chosed);
char change_direction(char current_direction, char anterior_direction, int snake_size, int chunk, int* current_pos, int*anterior_pos, int* fruit_pos, int** snake, int**next_snake, char* chosed) {
  printf("CURRENT %c\n", current_direction);
  printf("CURRENT position %d %d CURRENT fruit %d %d\n", current_pos[0], current_pos[1], fruit_pos[0], fruit_pos[1]);

  if (calculate_distance(current_pos, fruit_pos) > calculate_distance(anterior_pos, fruit_pos)){
    if (current_pos[0] > fruit_pos[0] && (current_direction == 'N' || current_direction == 'S')){
      char result = set_direction('W', anterior_direction, snake_size, chunk, false, current_pos, fruit_pos, snake, next_snake, chosed); 
      return result;

    } else if (current_pos[0] < fruit_pos[0] && (current_direction == 'N' || current_direction == 'S')){
      char result = set_direction('E', anterior_direction, snake_size, chunk, false, current_pos, fruit_pos, snake, next_snake, chosed);
      return result;

    } else if (current_pos[1] < fruit_pos[1] && (current_direction == 'W' || current_direction == 'E')){
      char result = set_direction('S', anterior_direction, snake_size, chunk, false, current_pos, fruit_pos, snake, next_snake, chosed);
      return result;

    } else if(current_pos[1] > fruit_pos[1] && (current_direction == 'W' || current_direction == 'E')){
      char result = set_direction('N', anterior_direction, snake_size, chunk, false, current_pos, fruit_pos, snake, next_snake, chosed);
      return result;

    }
  } else if (current_pos[1] == fruit_pos[1]){
    if ((current_direction == 'N' || current_direction == 'S') && current_pos[0] < fruit_pos[0]){
      return set_direction('E', anterior_direction, snake_size, chunk, false, current_pos, fruit_pos, snake, next_snake, chosed);
    } else if ((current_direction == 'N' || current_direction == 'S') && current_pos[0] > fruit_pos[0]){
      return set_direction('W', anterior_direction, snake_size, chunk, false, current_pos, fruit_pos, snake, next_snake, chosed);

    } else if(current_direction == 'E' && current_pos[0] > fruit_pos[0]){
      return set_direction('N', anterior_direction, snake_size, chunk, false, current_pos, fruit_pos, snake, next_snake, chosed);

    } else if(current_direction == 'W' && current_pos[0] < fruit_pos[0]){
      return set_direction('S', anterior_direction, snake_size, chunk, false, current_pos, fruit_pos, snake, next_snake, chosed);
    }
    
  } else if(current_pos[0] == fruit_pos[0]){
    if ((current_direction == 'E' || current_direction == 'W') && current_pos[1] > fruit_pos[1]){
      return set_direction('N', anterior_direction, snake_size, chunk, false, current_pos, fruit_pos, snake, next_snake, chosed);

    } else if((current_direction == 'E' || current_direction == 'W') && current_pos[1] < fruit_pos[1]){
      return set_direction('S', anterior_direction, snake_size, chunk, false, current_pos, fruit_pos, snake, next_snake, chosed);

    } else if (current_direction == 'N' && current_pos[1] < fruit_pos[1]){
      return set_direction('E', anterior_direction, snake_size, chunk, false, current_pos, fruit_pos, snake, next_snake, chosed);

    } else if (current_direction == 'S' && current_pos[1] > fruit_pos[1]){
      return set_direction('W', anterior_direction, snake_size, chunk, false, current_pos, fruit_pos, snake, next_snake, chosed);

    }

  }

  return set_direction(current_direction, anterior_direction, snake_size, chunk, false, current_pos, fruit_pos, snake, next_snake, chosed);

}

bool check_collision(char current_direction, int chunk, int snake_size, int* current_pos, int** next_snake){
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

  if (!check_position_in(next, next_snake, snake_size) && !check_position_out_of_board(next, 400)) {
    return true;
  } return false;

}

char compare_obstacles(char current_direction, char* others, int snake_size, int chunk, int**next_snake, int*next_pos, int* fruit_pos){
  double count = check_obstacles(current_direction, snake_size, next_snake, next_pos, fruit_pos);
  printf("COUNT %f CURRENT %c\n", count, current_direction);
  char result = current_direction;
  for (int i = 0; i < 3; i++){
    double inner = check_obstacles(others[i], snake_size, next_snake, next_pos, fruit_pos);
    printf("Others %f %c\n", inner, others[i]);
    if (inner < count && check_collision(others[i], chunk, snake_size, next_pos, next_snake)){
      count = inner;
      result = others[i];

    }
  
  } return result;

}

char set_direction(char current_direction, char anterior_direction, int snake_size, int chunk, bool away, int* current_pos, int* fruit_pos, int** snake, int**next_snake, char* chosed) {
    char* chosed_copy = chosed;
    find_and_remove(chosed_copy, current_direction);

    int chosed_lenght = strlen(chosed_copy);
    printf("CURRENT DIRECTION %c STRLEN %d\n", current_direction, chosed_lenght);
    printf("CHOSED %c\n", chosed_copy[0]);
    char exc;

    switch (current_direction){
      case('N'):
        exc = 'S';

      case('S'):
        exc = 'N';

      case('E'):
        exc = 'W';

      case('W'):
        exc = 'E';

    }

    if (check_collision(current_direction, chunk, snake_size, next_snake[snake_size-1], next_snake)){
      return compare_obstacles(current_direction, chosed_copy, snake_size, chunk, next_snake, current_pos, fruit_pos);
    }

    return set_direction(chosed_copy[0], current_direction, snake_size, chunk, away, current_pos, fruit_pos, snake, next_snake, chosed_copy);
      
}
