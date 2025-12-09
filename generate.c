#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *concat(char s1[], char s2[]) {
  char *result = malloc(strlen(s1) + strlen(s2) + 1);
  strcpy(result, s1);
  strcat(result, s2);
  return result;
}

int main(int argc, char **argv) {
  char *output = NULL;
  FILE *file = NULL;

  if (argc != 2) {
    fprintf(stderr, "missing output arg\n");
    return 1;
  }

  output = argv[1];

  file = fopen(output, "w");

  char html[] =
      "<!DOCTYPE html>\n"
      "<html lang=\"en\">\n"
      "<head>\n"
      " <meta charset=\"UTF-8\">\n"
      "  <meta name=\"viewport\" content=\"width=device-width, "
      "initial-scale=1.0\">\n"
      "  <meta http-equiv=\"X-UA-Compatible\" content=\"ie=edge\">\n"
      "  <title>Não Ouvo (Arquivo da Comunidade)</title>\n"
      "  <link rel=\"stylesheet\" href=\"./style.css\">\n"
      "  <link rel=\"icon\" href=\"./favicon.ico\" type=\"image/x-icon\">\n"
      "</head>\n"
      "<body>\n"
      " <main>\n"
      "   <h1>Não Ouvo (Arquivo da Comunidade)</h1>\n"
      "   <div id=\"episodes\">\n";
  char html_close[] = "   </div>\n"
                      " </main>\n"
                      "</body>\n";
  char *r = concat(html, html_close);

  fprintf(file, r);
  fclose(file);

  return 0;
}
