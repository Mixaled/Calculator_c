#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "parsers.c"

/*
(a + b)       +
a + b         +
a - b         +
a * b         +
a / b         +
a ^ b         +-
a mod b       +
+a            +
-a            +
cos(x)        +
sin(x)        +
tan(x)        +
acos(x)       +
asin(x)       +
atan(x)       +
sqrt(x)       +
ln(x)         +
log(x)        +
x             +
Graphics      +
Cleaning      +
ERR           +
Cross-os      TODO
Unit test     +-
decimal point +
bonus:
credit calc   TODO
deposite calc TODO
*/
#define panic(...)       \
  {                      \
    printf(__VA_ARGS__); \
    exit(1);             \
  }
void create_compile(char *expression) {
  char pow_expr[255];
  int set_start[100] = {0};
  int set_end[100] = {0};
  parser(expression, set_start, set_end);
  set_pow(expression, pow_expr, set_start, set_end);
  char new_expr[255];
  char clog[255];
  char final[255];
  parser_mod(pow_expr, new_expr);
  char casted[255];
  cast(new_expr, casted);
  parser_clog(casted, clog);
  parser_nlog(clog, final);
  printf("new_expr: %s\n", final);
  FILE *file = fopen("expression.c", "w");
  fprintf(file, "#include <stdio.h>\n\n");
  fprintf(file, "#include <math.h>\n\n");
  fprintf(file, "int main() {\n");
  fprintf(file, "    double result = %s;\n", final);
  fprintf(file, "    printf(\"%%lf\", result);\n");
  fprintf(file, "    return 0;\n");
  fprintf(file, "}\n");
  fclose(file);
}

void create_compile_x(char *expression) {
  char pow_expr[255];
  int set_start[100] = {0};
  int set_end[100] = {0};
  parser(expression, set_start, set_end);
  set_pow(expression, pow_expr, set_start, set_end);
  char new_expr[255];
  char clog[255];
  char final[255];
  parser_mod(pow_expr, new_expr);
  char casted[255];
  cast(new_expr, casted);
  parser_clog(casted, clog);
  parser_nlog(clog, final);
  printf("new_expr_x: %s\n", final);
  FILE *file = fopen("expression.c", "w");
  fprintf(file, "#include <stdio.h>\n\n");
  fprintf(file, "#include <stdlib.h>\n\n");
  fprintf(file, "#include <math.h>\n\n");
  fprintf(file, "int main(int argc, char *argv[]) {\n");
  fprintf(file, "    double x = atof(argv[1]);\n");
  fprintf(file, "    double result = %s;\n", final);
  fprintf(file, "    printf(\"%%lf\", result);\n");
  fprintf(file, "    return 0;\n");
  fprintf(file, "}\n");
  fclose(file);
}

void create_expression() {
  char compile_command[100];
  sprintf(compile_command, "gcc -shared -o expression.dll expression.c");
  system(compile_command);
}
// BONUS

void create_compile_credit(char *principal, char *annualRate,
                           char *loanDurationMonths) {
  FILE *file = fopen("expression.c", "w");
  fprintf(file, "#include <stdio.h>\n\n");
  fprintf(file, "#include <math.h>\n\n");
  fprintf(file, "double calculate() {\n");
  fprintf(file, "    double principal = %s;\n", principal);
  fprintf(file, "    double annualRate = %s;\n", annualRate);
  fprintf(file, "    double loanDurationMonths = %s;\n", loanDurationMonths);
  fprintf(file, "    double monthlyRate = (annualRate / 100) / 12;\n");
  fprintf(file,
          "    double monthlyPayment = principal * (monthlyRate * pow(1 + "
          "monthlyRate, loanDurationMonths))\n");
  fprintf(file,
          "                        / (pow(1 + monthlyRate, loanDurationMonths) "
          "- 1);\n");
  fprintf(file, "    return monthlyPayment;\n");
  fprintf(file, "}\n");
  fclose(file);
}