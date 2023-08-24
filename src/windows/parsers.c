#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int is_sign(char l) {
  if (l == '+' || l == '-' || l == '*' || l == '/' || l == '^' || l == '%')
    return 1;
  else
    return 0;
}

void replace_char(char* str, char find, char replace) {
  for (int i = 0; str[i] != '\0'; i++) {
    if (str[i] == find) {
      str[i] = replace;
    }
  }
}

void parser(char* expression, int* set_start, int* set_end) {
  int index = 0;
  int len = strlen(expression);
  for (int i = 0; i <= len; i++) {
    if (expression[i] == '^') {
      for (int j = i - 1; j >= 0; j--) {
        if (is_sign(expression[j]) || j == 0) {
          int start_pow = j == 0 ? 0 : j + 1;
          set_start[index] = start_pow;
          break;
        }
      }

      for (int j = i + 1; j <= len; j++) {
        if (is_sign(expression[j]) || expression[j] == '\0') {
          int end_pow = j;
          set_end[index] = end_pow;
          break;
        }
      }
      index++;
    }
  }
}

void set_pow(char* expression, char* new_expression, int* set_start,
             int* set_end) {
  int index = 0;
  int index2 = 0;
  int j = 0;
  if (set_end[0] != 0) {
    for (int i = 0; i <= strlen(expression) + 1; i++) {
      if (i == set_start[index]) {
        new_expression[j++] = 'p';
        new_expression[j++] = 'o';
        new_expression[j++] = 'w';
        new_expression[j++] = '(';
        index++;
      }
      if (i == set_end[index2]) {
        new_expression[j++] = ')';
        index2++;
      }
      new_expression[j++] = expression[i];
    }
  } else {
    strcpy(new_expression, expression);
  }
  replace_char(new_expression, '^', ',');
}

void parser_nlog(char* expression, char* new_expr) {
  int len = strlen(expression);
  int i = 0, j = 0;
  while (i < len) {
    if (expression[i] == 'l' && expression[i + 1] == 'n' && i < len - 2) {
      new_expr[j++] = 'l';
      new_expr[j++] = 'o';
      new_expr[j++] = 'g';
      i += 2;
    } else {
      new_expr[j++] = expression[i++];
    }
  }
  new_expr[j] = '\0';
}

void parser_clog(char* expression, char* new_expr) {
  int len = strlen(expression);
  int i = 0, j = 0;
  while (i < len) {
    if (expression[i] == 'l' && expression[i + 1] == 'o' &&
        expression[i + 2] == 'g' && i < len - 2) {
      new_expr[j++] = 'l';
      new_expr[j++] = 'o';
      new_expr[j++] = 'g';
      new_expr[j++] = '1';
      new_expr[j++] = '0';
      i += 3;
    } else {
      new_expr[j++] = expression[i++];
    }
  }
  new_expr[j] = '\0';
}

void parser_mod(char* expression, char* new_expr) {
  int expr_len = strlen(expression);
  int i = 0, j = 0;
  while (i < expr_len) {
    if (expression[i] == 'm' && i < expr_len - 2) {
      new_expr[j++] = '%';
      i += 3;
    } else {
      new_expr[j++] = expression[i++];
    }
  }
  new_expr[j] = '\0';
}
int containsChar(const char* str, char target) {
  while (*str != '\0') {
    if (*str == target) {
      return 1;
    }
    str++;
  }
  return 0;
}

int cast(char* str, char* new_str) {
  int index = 0;
  int j = 0;
  int stage = 0;
  int comma = 0;
  for (int i = 0; i <= strlen(str); i++) {
    if (containsChar(str, '%')) {
      comma = 1;
      break;
    }
    if (str[i] == '.') {
      comma = 1;
      break;
    }
    if (isdigit(str[i])) {
      stage = 1;
    }
    if (is_sign(str[i]) == 1 && stage == 1 || str[i] == ')') {
      stage = stage + 1;
      index = i;
      break;
    }
  }
  if (stage == 2 && comma != 1) {
    for (int i = 0; i <= strlen(str); i++) {
      if (i == index) {
        new_str[j++] = '.';
        new_str[j++] = '0';
        new_str[j++] = str[i];
      } else {
        new_str[j++] = str[i];
      }
    }
  } else {
    for (int i = 0; i <= strlen(str); i++) {
      new_str[j++] = str[i];
    }
  }
}