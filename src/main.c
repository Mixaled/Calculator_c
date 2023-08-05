#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h> 
#include <unistd.h>


/*
(a + b)  +
a + b    +
a - b    +
a * b    +
a / b    +
a ^ b    todo
a mod b  +
+a       todo
-a       todo
cos(x)   +
sin(x)   +
tan(x)   +
acos(x)  +
asin(x)  +
atan(x)  +
sqrt(x)  +
ln(x)    todo
log(x)   todo
x        +
Graphics +
Cleaning +
Docker or rp TODO

/*
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int is_sign(char l) {
    if (l == '+' || l == '-' || l == '*' || l == '/' || l == '^')
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

void insert_string(char* original, char* inserted, int index, char* result) {
    int orig_len = strlen(original);
    int insert_len = strlen(inserted);
    strncpy(result, original, index);
    strcpy(result + index, inserted);
    strcpy(result + index + insert_len, original + index);
}


void parser(char* expression, char* new_expr) {
    strcpy(new_expr, expression);
    printf("string: %s\n", new_expr);
    int len = strlen(expression);
    char* buffer = (char*)malloc((len+5) * sizeof(char));
    for (int i = 0; i < len; i++) {
        if (expression[i] == '^') {
            replace_char(new_expr, '^', ',');
            printf("index ^: %d\n", i);
            for (int j = i - 1; j >= 0; j--) {
                if (is_sign(expression[j]) == 1) {
                    printf("index of start: %d\n", j);
                    int start_pow = j+1;
                    insert_string(new_expr, "pow(", start_pow, buffer);
                    char* tmp = buffer;
                    buffer = new_expr;
                    new_expr = tmp;
                    break;
                }
            }
            for (int j = i + 1; j <= len; j++) {
                if (is_sign(expression[j]) == 1) {
                    printf("index of end: %d\n", j);
                    int end_pow = j;
                    insert_string(new_expr, ")", end_pow+(end_pow-i)+1, buffer);
                    char* tmp = buffer;
                    buffer = new_expr;
                    new_expr = tmp;
                    break;
                }
            }
        }
    }
}

int main() {
    char original[] = "Hello,  World!";
    char inserted[] = "Beautiful";
    int index = 7;

    int orig_len = strlen(original);
    int insert_len = strlen(inserted);
    char* result = (char*)malloc((orig_len + insert_len + 1) * sizeof(char));
    insert_string(original, inserted, index, result);
    printf("%s\n", result);
    free(result);

    char* b = (char*)malloc((orig_len + insert_len + 1) * sizeof(char));
    parser("2^3^4", b);
    printf("result: %s\n", b);
    return 0;
}

*/
#define panic(...)  { printf(__VA_ARGS__); exit(1); }
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

int is_sign(char l) {
  if (l == '+' || l == '-' || l == '*' || l == '/' || l == '^' || l == '%')
    return 1;
  else
    return 0;
}

int check_expression(char* expression) {
  int len = strlen(expression);
  int signs = 0;
  for (int i = 0; i < len; i++) {
    if (is_sign(expression[i]) == 1) {
      signs++;
    } else {
      signs = 0;
    }
    if (signs == 2) {
      printf("Error: Two signs in a row\n");
      return 1;
    }
  }
  return 0;
}

__declspec(dllexport) void create_compile(char* expression) {
  int res = check_expression(expression);
  char new_expr[255]; 
  parser_mod(expression, new_expr);
  printf("new_expr: %s\n",new_expr);
  if (res == 0) {
    FILE* file = fopen("expression.c", "w");
    fprintf(file, "#include <stdio.h>\n\n");
    fprintf(file, "#include <math.h>\n\n");
    fprintf(file, "__declspec(dllexport) double calculate() {\n");
    fprintf(file, "    double result = %s;\n", new_expr);
    fprintf(file, "    return result;\n");
    fprintf(file, "}\n");
    fclose(file);
  }
}

__declspec(dllexport) void create_compile_x(char* expression) {
  int res = check_expression(expression);
  char new_expr[255]; 
  parser_mod(expression, new_expr);
  printf("new_expr_x: %s\n",new_expr);
  if (res == 0) {
    FILE* file = fopen("expression.c", "w");
    fprintf(file, "#include <stdio.h>\n\n");
    fprintf(file, "#include <math.h>\n\n");
    fprintf(file, "__declspec(dllexport) double calculate(double x) {\n");
    fprintf(file, "    double result = %s;\n", new_expr);
    fprintf(file, "    return result;\n");
    fprintf(file, "}\n");
    fclose(file);
  }
}

__declspec(dllexport) void create_expression(char* number) {
  char compile_command[100];
  sprintf(compile_command, "gcc -shared -o expression%s.dll expression.c",
          number);
  system(compile_command);
}