#include <check.h>

#include "expression.c"
#include "parsers.c"

START_TEST(test_is_sign) {
  ck_assert_int_eq(is_sign('+'), 1);
  ck_assert_int_eq(is_sign('-'), 1);
  ck_assert_int_eq(is_sign('*'), 1);
  ck_assert_int_eq(is_sign('/'), 1);
  ck_assert_int_eq(is_sign('%'), 1);
}
END_TEST

START_TEST(test_replace_char) {
  char str[] = "34+56+44+33+44";
  replace_char(str, '+', '*');
  ck_assert_str_eq(str, "34*56*44*33*44");
}
END_TEST

START_TEST(test_parser_and_set_pow1) {
  char expression[] = "2^3+4^5*6^7";
  int set_start[10] = {0};
  int set_end[10] = {0};

  parser(expression, set_start, set_end);
  char new_expression[100];
  set_pow(expression, new_expression, set_start, set_end);
  ck_assert_str_eq(new_expression, "pow(2,3)+pow(4,5)*pow(6,7)");
}

END_TEST

START_TEST(test_parser_and_set_pow2) {
  char expression[] = "2^x";
  int set_start[10] = {0};
  int set_end[10] = {0};

  parser(expression, set_start, set_end);
  char new_expression[100];
  set_pow(expression, new_expression, set_start, set_end);
  ck_assert_str_eq(new_expression, "pow(2,x)");
}

START_TEST(test_parser_and_set_pow3) {
  char expression[] = "2*x";
  int set_start[10] = {0};
  int set_end[10] = {0};

  parser(expression, set_start, set_end);
  char new_expression[100];
  set_pow(expression, new_expression, set_start, set_end);
  ck_assert_str_eq(new_expression, "2*x");
}

END_TEST

START_TEST(test_parser_clog) {
  char expression[] = "log(x)+log(100)+log(y)";
  char new_expr[100];

  parser_clog(expression, new_expr);

  ck_assert_str_eq(new_expr, "log10(x)+log10(100)+log10(y)");
}
END_TEST

START_TEST(test_parser_nlog) {
  char expression[] = "ln(x)+ln(100)+ln(y)";
  char new_expr[100];

  parser_nlog(expression, new_expr);

  ck_assert_str_eq(new_expr, "log(x)+log(100)+log(y)");
}
END_TEST

START_TEST(test_parser_mod) {
  char expression[] = "10mod3+5mod2+mod1";
  char new_expr[100];

  parser_mod(expression, new_expr);

  ck_assert_str_eq(new_expr, "10%3+5%2+%1");
}
END_TEST

START_TEST(gcc_check) {
  printf("I belive in GCC\n");
  double expression = 9.0 / 6.0;
  double new_expr = 9.0 / 6.0;
  ck_assert_double_eq(expression, new_expr);
}
END_TEST

START_TEST(test_cast) {
  char input[] = "12+34";
  char output[100];
  cast(input, output);
  ck_assert_str_eq(output, "12.0+34");
  char input2[] = "12.34+56";
  char output2[100];
  cast(input2, output2);
  ck_assert_str_eq(output2, "12.34+56");
  char input3[] = "12.+34";
  char output3[100];
  cast(input3, output3);
  ck_assert_str_eq(output3, "12.+34");
  char input4[] = "12+34%8";
  char output4[100];
  cast(input4, output4);
  ck_assert_str_eq(output4, "12+34%8");
}
END_TEST

Suite *test_suite(void) {
  Suite *s;
  TCase *tc_core;

  s = suite_create("Parsers");

  tc_core = tcase_create("Core");
  tcase_add_test(tc_core, test_is_sign);
  tcase_add_test(tc_core, test_replace_char);
  tcase_add_test(tc_core, test_parser_and_set_pow1);
  tcase_add_test(tc_core, test_parser_and_set_pow2);
  tcase_add_test(tc_core, test_parser_and_set_pow3);
  tcase_add_test(tc_core, test_parser_mod);
  tcase_add_test(tc_core, test_parser_clog);
  tcase_add_test(tc_core, test_parser_nlog);
  tcase_add_test(tc_core, test_cast);
  tcase_add_test(tc_core, gcc_check);
  suite_add_tcase(s, tc_core);

  return s;
}

int main(void) {
  int number_failed;
  Suite *s;
  SRunner *sr;

  s = test_suite();
  sr = srunner_create(s);

  srunner_run_all(sr, CK_NORMAL);
  number_failed = srunner_ntests_failed(sr);
  srunner_free(sr);

  return (number_failed == 0) ? EXIT_SUCCESS : EXIT_FAILURE;
}