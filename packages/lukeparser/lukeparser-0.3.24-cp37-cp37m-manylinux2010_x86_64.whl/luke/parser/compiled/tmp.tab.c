/* A Bison parser, made by GNU Bison 3.4.  */

/* Bison implementation for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2019 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Undocumented macros, especially those whose name start with YY_,
   are private implementation details.  Do not rely on them.  */

/* Identify Bison output.  */
#define YYBISON 1

/* Bison version.  */
#define YYBISON_VERSION "3.4"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 2

/* Push parsers.  */
#define YYPUSH 1

/* Pull parsers.  */
#define YYPULL 0

/* "%code top" blocks.  */
#line 1 "src/luke/parser/compiled/tmp.y"


#include "tmp.tab.h"
#include "lex.yy.h"
#include "Python.h"
void *(*py_callback)(void *, char *, int, int, ...);
void (*py_input)(void *, char *, int *, int);
void *py_parser;
__attribute__ ((dllexport)) char *rules_hash = "6417c83592df7b96b88fa0277954f26c2b315b51";
#define YYERROR_VERBOSE 1


#line 80 "tmp.tab.c"




# ifndef YY_NULLPTR
#  if defined __cplusplus
#   if 201103L <= __cplusplus
#    define YY_NULLPTR nullptr
#   else
#    define YY_NULLPTR 0
#   endif
#  else
#   define YY_NULLPTR ((void*)0)
#  endif
# endif

/* Enabling verbose error messages.  */
#ifdef YYERROR_VERBOSE
# undef YYERROR_VERBOSE
# define YYERROR_VERBOSE 1
#else
# define YYERROR_VERBOSE 0
#endif

/* Use api.header.include to #include this header
   instead of duplicating it here.  */
#ifndef YY_YY_TMP_TAB_H_INCLUDED
# define YY_YY_TMP_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 1
#endif
#if YYDEBUG
extern int yydebug;
#endif
/* "%code requires" blocks.  */
#line 14 "src/luke/parser/compiled/tmp.y"


typedef void * yyscan_t;
#define YYLTYPE YYLTYPE
typedef struct YYLTYPE
{
  int first_line;
  int first_column;
  int last_line;
  int last_column;
  char *filename;
} YYLTYPE;

void yyerror(YYLTYPE *locp, yyscan_t scanner, char const *msg);

#line 133 "tmp.tab.c"

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    FOOTNOTE_START = 258,
    FOOTNOTE_MID = 259,
    FOOTNOTE_INLINE_START = 260,
    FOOTNOTE_INLINE_MID = 261,
    IMG_START = 262,
    LINK_START = 263,
    HYPERREF_LINK_CHAR = 264,
    HYPERREF_LINK_ALT_CHAR = 265,
    HYPERREF_LINK_ALT_END = 266,
    HYPERREF_LINK_ALT_START = 267,
    HYPERREF_LINK_END = 268,
    HYPERREF_LINK_MID = 269,
    LINK_DEFINITION = 270,
    IMAGE_DEFINITION = 271,
    FOOTNOTE_DEFINITION = 272,
    HYPERREF_REF_MID = 273,
    HYPERREF_REF_END = 274,
    HYPERREF_CODE_START = 275,
    HYPERREF_CODE_CHAR = 276,
    HYPERREF_CODE_END = 277,
    HEADINGHASH = 278,
    HEADINGHASH_END = 279,
    HEADING_ULINEDBL = 280,
    HEADING_ULINESGL = 281,
    ULIST_SYM = 282,
    OLIST_SYM = 283,
    QUOTE_SYM = 284,
    INDENT_SYM = 285,
    EMPH_START = 286,
    EMPH_END = 287,
    STRONG_START = 288,
    STRONG_END = 289,
    STRIKE_START = 290,
    STRIKE_END = 291,
    ITALIC_START = 292,
    ITALIC_END = 293,
    BOLD_START = 294,
    BOLD_END = 295,
    BR = 296,
    CHAR = 297,
    NEWLINE = 298,
    ATTR_START = 299,
    ATTR_END = 300,
    ATTR_END_AND_ARG_START = 301,
    ATTR_INPUT = 302,
    ATTR_HASH = 303,
    ATTR_DOT = 304,
    ATTR_EXCLAMATION = 305,
    ATTR_COMMA = 306,
    ATTR_EQUAL = 307,
    ATTR_BOOLEAN = 308,
    ATTR_NUMBER = 309,
    ATTR_STRING = 310,
    ATTR_WORD = 311,
    ATTR_PLACEHOLDER = 312,
    CODEBLOCK_START = 313,
    CODEBLOCK_END = 314,
    CODEBLOCK_STRING_BEFORE = 315,
    CODEBLOCK_BR = 316,
    CODEBLOCK_CHAR = 317,
    CODEINLINE_START = 318,
    CODEINLINE_CHAR = 319,
    CODEINLINE_END = 320,
    MATHBLOCK_START = 321,
    MATHINLINE_START = 322,
    MATHBLOCK_CHAR = 323,
    MATH_END = 324,
    TABLE_DELIM = 325,
    TABLE_HRULE = 326,
    TABLE_HRULE_CENTERED = 327,
    TABLE_HRULE_LEFT_ALIGNED = 328,
    TABLE_HRULE_RIGHT_ALIGNED = 329,
    LATEX_COMMAND = 330,
    LATEX_COMMAND_WITH_ARGUMENTS = 331,
    PLACEHOLDER = 332,
    LATEX_COMMAND_WITH_OPTIONAL_ARGUMENT = 333,
    MATHBLOCK_LATEX_COMMAND = 334,
    MATHBLOCK_CURLY_OPEN = 335,
    MATHBLOCK_CURLY_CLOSE = 336,
    MATHBLOCK_VERBATIM_PLACEHOLDER = 337,
    URL = 338,
    HRULE = 339,
    UNEXPECTED_END = 340
  };
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef void * YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif

/* Location type.  */
#if ! defined YYLTYPE && ! defined YYLTYPE_IS_DECLARED
typedef struct YYLTYPE YYLTYPE;
struct YYLTYPE
{
  int first_line;
  int first_column;
  int last_line;
  int last_column;
};
# define YYLTYPE_IS_DECLARED 1
# define YYLTYPE_IS_TRIVIAL 1
#endif



#ifndef YYPUSH_MORE_DEFINED
# define YYPUSH_MORE_DEFINED
enum { YYPUSH_MORE = 4 };
#endif

typedef struct yypstate yypstate;

int yypush_parse (yypstate *ps, int pushed_char, YYSTYPE const *pushed_val, YYLTYPE *pushed_loc, yyscan_t scanner);

yypstate * yypstate_new (void);
void yypstate_delete (yypstate *ps);

#endif /* !YY_YY_TMP_TAB_H_INCLUDED  */



#ifdef short
# undef short
#endif

#ifdef YYTYPE_UINT8
typedef YYTYPE_UINT8 yytype_uint8;
#else
typedef unsigned char yytype_uint8;
#endif

#ifdef YYTYPE_INT8
typedef YYTYPE_INT8 yytype_int8;
#else
typedef signed char yytype_int8;
#endif

#ifdef YYTYPE_UINT16
typedef YYTYPE_UINT16 yytype_uint16;
#else
typedef unsigned short yytype_uint16;
#endif

#ifdef YYTYPE_INT16
typedef YYTYPE_INT16 yytype_int16;
#else
typedef short yytype_int16;
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif ! defined YYSIZE_T
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned
# endif
#endif

#define YYSIZE_MAXIMUM ((YYSIZE_T) -1)

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(Msgid) dgettext ("bison-runtime", Msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(Msgid) Msgid
# endif
#endif

#ifndef YY_ATTRIBUTE
# if (defined __GNUC__                                               \
      && (2 < __GNUC__ || (__GNUC__ == 2 && 96 <= __GNUC_MINOR__)))  \
     || defined __SUNPRO_C && 0x5110 <= __SUNPRO_C
#  define YY_ATTRIBUTE(Spec) __attribute__(Spec)
# else
#  define YY_ATTRIBUTE(Spec) /* empty */
# endif
#endif

#ifndef YY_ATTRIBUTE_PURE
# define YY_ATTRIBUTE_PURE   YY_ATTRIBUTE ((__pure__))
#endif

#ifndef YY_ATTRIBUTE_UNUSED
# define YY_ATTRIBUTE_UNUSED YY_ATTRIBUTE ((__unused__))
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YYUSE(E) ((void) (E))
#else
# define YYUSE(E) /* empty */
#endif

#if defined __GNUC__ && ! defined __ICC && 407 <= __GNUC__ * 100 + __GNUC_MINOR__
/* Suppress an incorrect diagnostic about yylval being uninitialized.  */
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN \
    _Pragma ("GCC diagnostic push") \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")\
    _Pragma ("GCC diagnostic ignored \"-Wmaybe-uninitialized\"")
# define YY_IGNORE_MAYBE_UNINITIALIZED_END \
    _Pragma ("GCC diagnostic pop")
#else
# define YY_INITIAL_VALUE(Value) Value
#endif
#ifndef YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_END
#endif
#ifndef YY_INITIAL_VALUE
# define YY_INITIAL_VALUE(Value) /* Nothing. */
#endif


#define YY_ASSERT(E) ((void) (0 && (E)))

#if ! defined yyoverflow || YYERROR_VERBOSE

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's 'empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (0)
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined EXIT_SUCCESS \
       && ! ((defined YYMALLOC || defined malloc) \
             && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef EXIT_SUCCESS
#    define EXIT_SUCCESS 0
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined EXIT_SUCCESS
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined EXIT_SUCCESS
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* ! defined yyoverflow || YYERROR_VERBOSE */


#if (! defined yyoverflow \
     && (! defined __cplusplus \
         || (defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL \
             && defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yytype_int16 yyss_alloc;
  YYSTYPE yyvs_alloc;
  YYLTYPE yyls_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (sizeof (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (sizeof (yytype_int16) + sizeof (YYSTYPE) + sizeof (YYLTYPE)) \
      + 2 * YYSTACK_GAP_MAXIMUM)

# define YYCOPY_NEEDED 1

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)                           \
    do                                                                  \
      {                                                                 \
        YYSIZE_T yynewbytes;                                            \
        YYCOPY (&yyptr->Stack_alloc, Stack, yysize);                    \
        Stack = &yyptr->Stack_alloc;                                    \
        yynewbytes = yystacksize * sizeof (*Stack) + YYSTACK_GAP_MAXIMUM; \
        yyptr += yynewbytes / sizeof (*yyptr);                          \
      }                                                                 \
    while (0)

#endif

#if defined YYCOPY_NEEDED && YYCOPY_NEEDED
/* Copy COUNT objects from SRC to DST.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(Dst, Src, Count) \
      __builtin_memcpy (Dst, Src, (Count) * sizeof (*(Src)))
#  else
#   define YYCOPY(Dst, Src, Count)              \
      do                                        \
        {                                       \
          YYSIZE_T yyi;                         \
          for (yyi = 0; yyi < (Count); yyi++)   \
            (Dst)[yyi] = (Src)[yyi];            \
        }                                       \
      while (0)
#  endif
# endif
#endif /* !YYCOPY_NEEDED */

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  132
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   3150

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  86
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  52
/* YYNRULES -- Number of rules.  */
#define YYNRULES  194
/* YYNSTATES -- Number of states.  */
#define YYNSTATES  274

#define YYUNDEFTOK  2
#define YYMAXUTOK   340

/* YYTRANSLATE(TOKEN-NUM) -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex, with out-of-bounds checking.  */
#define YYTRANSLATE(YYX)                                                \
  ((unsigned) (YYX) <= YYMAXUTOK ? yytranslate[YYX] : YYUNDEFTOK)

/* YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex.  */
static const yytype_uint8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,    48,    49,    50,    51,    52,    53,    54,
      55,    56,    57,    58,    59,    60,    61,    62,    63,    64,
      65,    66,    67,    68,    69,    70,    71,    72,    73,    74,
      75,    76,    77,    78,    79,    80,    81,    82,    83,    84,
      85
};

#if YYDEBUG
  /* YYRLINE[YYN] -- Source line where rule number YYN was defined.  */
static const yytype_uint16 yyrline[] =
{
       0,    44,    44,    45,    46,    62,    63,    64,    80,    81,
      82,    92,   106,   107,   108,   118,   132,   133,   134,   144,
     158,   159,   160,   170,   184,   185,   186,   196,   207,   224,
     238,   253,   269,   284,   299,   315,   329,   348,   362,   376,
     390,   404,   418,   432,   446,   460,   474,   488,   502,   518,
     532,   546,   561,   580,   594,   612,   630,   646,   661,   676,
     693,   709,   724,   739,   756,   772,   787,   802,   819,   834,
     849,   865,   881,   896,   913,   927,   943,   959,   974,   992,
    1008,  1023,  1041,  1055,  1070,  1085,  1104,  1118,  1134,  1150,
    1166,  1182,  1198,  1212,  1228,  1242,  1256,  1270,  1285,  1300,
    1315,  1330,  1345,  1362,  1376,  1394,  1408,  1425,  1441,  1455,
    1471,  1487,  1503,  1517,  1534,  1550,  1566,  1583,  1597,  1613,
    1630,  1644,  1658,  1672,  1686,  1704,  1720,  1736,  1751,  1769,
    1785,  1804,  1820,  1839,  1855,  1874,  1888,  1902,  1916,  1930,
    1948,  1966,  1986,  2004,  2020,  2034,  2050,  2066,  2084,  2102,
    2120,  2134,  2151,  2165,  2182,  2198,  2217,  2231,  2246,  2262,
    2282,  2296,  2310,  2324,  2342,  2356,  2376,  2395,  2413,  2431,
    2448,  2465,  2484,  2498,  2513,  2530,  2546,  2561,  2576,  2591,
    2607,  2623,  2639,  2655,  2671,  2687,  2703,  2721,  2737,  2751,
    2765,  2779,  2793,  2810,  2824
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || 0
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "FOOTNOTE_START", "FOOTNOTE_MID",
  "FOOTNOTE_INLINE_START", "FOOTNOTE_INLINE_MID", "IMG_START",
  "LINK_START", "HYPERREF_LINK_CHAR", "HYPERREF_LINK_ALT_CHAR",
  "HYPERREF_LINK_ALT_END", "HYPERREF_LINK_ALT_START", "HYPERREF_LINK_END",
  "HYPERREF_LINK_MID", "LINK_DEFINITION", "IMAGE_DEFINITION",
  "FOOTNOTE_DEFINITION", "HYPERREF_REF_MID", "HYPERREF_REF_END",
  "HYPERREF_CODE_START", "HYPERREF_CODE_CHAR", "HYPERREF_CODE_END",
  "HEADINGHASH", "HEADINGHASH_END", "HEADING_ULINEDBL", "HEADING_ULINESGL",
  "ULIST_SYM", "OLIST_SYM", "QUOTE_SYM", "INDENT_SYM", "EMPH_START",
  "EMPH_END", "STRONG_START", "STRONG_END", "STRIKE_START", "STRIKE_END",
  "ITALIC_START", "ITALIC_END", "BOLD_START", "BOLD_END", "BR", "CHAR",
  "NEWLINE", "ATTR_START", "ATTR_END", "ATTR_END_AND_ARG_START",
  "ATTR_INPUT", "ATTR_HASH", "ATTR_DOT", "ATTR_EXCLAMATION", "ATTR_COMMA",
  "ATTR_EQUAL", "ATTR_BOOLEAN", "ATTR_NUMBER", "ATTR_STRING", "ATTR_WORD",
  "ATTR_PLACEHOLDER", "CODEBLOCK_START", "CODEBLOCK_END",
  "CODEBLOCK_STRING_BEFORE", "CODEBLOCK_BR", "CODEBLOCK_CHAR",
  "CODEINLINE_START", "CODEINLINE_CHAR", "CODEINLINE_END",
  "MATHBLOCK_START", "MATHINLINE_START", "MATHBLOCK_CHAR", "MATH_END",
  "TABLE_DELIM", "TABLE_HRULE", "TABLE_HRULE_CENTERED",
  "TABLE_HRULE_LEFT_ALIGNED", "TABLE_HRULE_RIGHT_ALIGNED", "LATEX_COMMAND",
  "LATEX_COMMAND_WITH_ARGUMENTS", "PLACEHOLDER",
  "LATEX_COMMAND_WITH_OPTIONAL_ARGUMENT", "MATHBLOCK_LATEX_COMMAND",
  "MATHBLOCK_CURLY_OPEN", "MATHBLOCK_CURLY_CLOSE",
  "MATHBLOCK_VERBATIM_PLACEHOLDER", "URL", "HRULE", "UNEXPECTED_END",
  "$accept", "string", "string2", "mathblock_string", "mathblock_string2",
  "hyperref_code_string", "hyperref_code_string2", "codeinline_string",
  "codeinline_string2", "hyperref_link_string", "hyperref_link_string2",
  "hyperref_link_alt_string", "hyperref_link_alt_string2",
  "codeblock_string", "codeblock_string2", "input_start", "input",
  "blocks", "block", "br", "br_end", "indent", "quote", "ulist", "olist",
  "href_definition", "header", "header_hash", "text", "span",
  "span_multitext_wrap", "span_multitext", "latex",
  "latex_command_with_arguments_and_optional",
  "latex_command_with_arguments", "table", "table_delim", "table_no_delim",
  "table_delim_separator", "table_no_delim_separator", "table_alignment",
  "hyperref", "hyperref_start", "math", "mathblock_text", "mathblock_span",
  "mathblock_latex", "codeblock_block", "attributes", "attribute_list",
  "attribute", "attribute_varname", YY_NULLPTR
};
#endif

# ifdef YYPRINT
/* YYTOKNUM[NUM] -- (External) token number corresponding to the
   (internal) symbol number NUM (which must be that of a token).  */
static const yytype_uint16 yytoknum[] =
{
       0,   256,   257,   258,   259,   260,   261,   262,   263,   264,
     265,   266,   267,   268,   269,   270,   271,   272,   273,   274,
     275,   276,   277,   278,   279,   280,   281,   282,   283,   284,
     285,   286,   287,   288,   289,   290,   291,   292,   293,   294,
     295,   296,   297,   298,   299,   300,   301,   302,   303,   304,
     305,   306,   307,   308,   309,   310,   311,   312,   313,   314,
     315,   316,   317,   318,   319,   320,   321,   322,   323,   324,
     325,   326,   327,   328,   329,   330,   331,   332,   333,   334,
     335,   336,   337,   338,   339,   340
};
# endif

#define YYPACT_NINF -159

#define yypact_value_is_default(Yystate) \
  (!!((Yystate) == (-159)))

#define YYTABLE_NINF -131

#define yytable_value_is_error(Yytable_value) \
  0

  /* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
     STATE-NUM.  */
static const yytype_int16 yypact[] =
{
     376,   -83,   -21,   712,  -159,  -159,   -30,   -20,  1559,    11,
    2925,  1610,  1661,  1712,  2577,  1019,  1019,  1019,  1019,  1019,
    -159,  -159,  -159,   290,   -35,   -18,    91,    91,  2626,  -159,
    -159,  -159,  -159,  -159,  -159,  -159,   290,  -159,  -159,  -159,
      23,    48,  -159,    18,  -159,   291,  -159,  -159,  -159,  -159,
    -159,  -159,  -159,  -159,  1289,  -159,  -159,   544,   628,  -159,
    1343,   -10,   -22,    12,    14,  -159,   460,  -159,   260,  1208,
    -159,    49,   -12,    67,  1763,  1814,   -83,  1865,  2974,  -159,
    1916,  1967,  2222,  2018,  2273,  2069,  2324,  2577,  1397,  -159,
    2675,   965,  1073,    62,  -159,    64,    61,    65,    59,    46,
      50,    51,  -159,  -159,  -159,  -159,  -159,  -159,  3014,  -159,
      53,   -14,    42,    70,  -159,    44,    60,  -159,  -159,    86,
    -159,  -159,    45,    41,    91,    54,    56,  -159,  2724,    66,
    1209,  -159,  -159,   291,  -159,  1127,  -159,    18,  -159,  -159,
    2925,  -159,  2778,  3002,    24,  3065,    52,  -159,  2827,  2925,
      69,   -22,   -22,   -22,   215,   121,   123,  -159,  -159,  -159,
    -159,  -159,  2120,  2171,  2974,  2375,  2426,  2477,  2528,  2876,
     101,  -159,   965,  -159,  -159,  -159,  -159,  -159,  -159,  -159,
    -159,  -159,   290,  -159,  1129,    42,    83,  -159,    87,    85,
      42,  -159,  -159,  -159,    68,  -159,  -159,  -159,    91,  -159,
    -159,  -159,  -159,  -159,  -159,  -159,  -159,  1451,  -159,  -159,
    -159,  -159,  -159,  -159,  -159,  -159,  1505,  -159,  -159,  -159,
    -159,   -21,   796,   136,   -21,   129,  -159,  -159,   880,  -159,
    -159,  -159,  -159,  -159,  -159,  -159,    96,    42,  -159,  -159,
     102,    91,    79,   153,   157,  -159,    63,   168,   161,  -159,
     159,   162,   -12,   166,  -159,   127,  -159,  -159,  -159,  -159,
    -159,   177,  -159,  -159,  -159,  -159,  -159,  -159,  -159,  -159,
     179,   178,  -159,  -159
};

  /* YYDEFACT[STATE-NUM] -- Default reduction number in state STATE-NUM.
     Performed when YYTABLE does not specify something else to do.  Zero
     means the default is an error.  */
static const yytype_uint8 yydefact[] =
{
       0,    48,     0,     0,   153,   152,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
      49,     3,    50,   175,     0,    15,     0,     0,     0,   135,
     136,   137,   138,   108,   117,    96,   175,   144,    43,    86,
       2,     0,    28,    29,    35,     0,    33,    42,    41,    39,
      40,    47,    37,    74,     0,    82,    95,     0,     0,    45,
       0,   121,   122,   123,     0,    94,     0,    92,     0,     0,
     102,     0,   151,     0,     0,     0,     0,     0,     0,    81,
       0,     0,     0,     0,     0,     0,     0,     0,     0,   124,
       0,     0,     0,    97,   103,    98,   101,    99,   100,     0,
       0,     0,   188,   189,   194,   193,   191,   192,     0,   172,
     190,     0,    27,     0,    13,     0,    12,     6,   164,     0,
     162,   160,     5,     0,   156,   161,     0,   127,     0,     0,
       0,     4,     1,     0,    30,     0,    51,    32,    77,    78,
       0,    84,     0,   113,     0,   112,     0,   128,     0,     0,
       0,     0,     0,     0,   150,    86,     0,   170,    83,   139,
     145,   146,     0,     0,     0,     0,     0,     0,     0,     0,
       0,   104,     0,    87,    88,    91,    89,    90,   176,   177,
     178,   171,     0,   173,     0,    27,     0,    25,     0,    24,
      27,    93,    14,   163,     0,     7,   154,   157,     0,   155,
     125,   131,   110,   114,    36,    52,    31,     0,    75,    76,
      85,   115,   111,   118,   109,   126,     0,   132,   134,   133,
     143,     0,     0,    19,     0,    11,   106,   174,     0,   179,
     180,   181,   182,   184,   185,   183,     0,    27,   169,    26,
       0,   158,     0,     0,     0,    17,     0,    16,     0,     9,
       0,     8,   187,     0,   167,     0,   168,   159,   165,   147,
     148,    23,   140,    18,   142,   149,    10,   186,   166,    21,
       0,    20,   141,    22
};

  /* YYPGOTO[NTERM-NUM].  */
static const yytype_int16 yypgoto[] =
{
    -159,     6,  -159,  -159,  -159,  -159,  -159,  -159,  -159,  -159,
    -159,  -159,  -159,  -158,  -159,  -159,    -2,   147,    76,     1,
     -37,  -159,  -159,  -159,  -159,  -159,  -159,   184,   104,   120,
      22,   -81,  -159,  -159,  -159,    -9,  -159,  -159,  -159,  -159,
       5,  -159,  -159,    10,   -23,  -159,  -159,  -159,     0,   160,
     -93,  -159
};

  /* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int16 yydefgoto[] =
{
      -1,    39,    40,   121,   122,   250,   251,   115,   116,   246,
     247,   270,   271,   188,   189,    41,    42,    43,    44,    45,
      46,    47,    48,    49,    50,    51,    52,    53,    54,    55,
      93,    94,    56,    57,    58,    59,    60,    61,    62,    63,
      64,    65,    66,    67,   123,   124,   125,    68,    78,   108,
     109,   110
};

  /* YYTABLE[YYPACT[STATE-NUM]] -- What to do in state STATE-NUM.  If
     positive, shift that token.  If negative, reduce the rule whose
     number is the opposite.  If YYTABLE_NINF, syntax error.  */
static const yytype_int16 yytable[] =
{
      69,    73,    70,    69,   126,    89,   134,   -48,    71,    23,
     171,    82,    84,    86,    90,   183,    91,    91,    91,    91,
      91,    21,    23,   107,   113,   111,   112,   236,    90,   -48,
      23,   -48,   240,   129,     9,    10,   107,   183,    95,    96,
      97,    98,   211,   212,   133,    69,   114,   185,   132,    29,
      30,    31,    32,    74,   142,   144,   146,    69,    69,    20,
     149,    22,   151,    75,   156,   131,    69,   150,   160,   151,
     213,   214,   155,    70,   159,   261,   262,   164,    89,   255,
     165,   166,   152,   167,   153,   168,   161,    90,   164,   227,
     151,   226,   164,   172,   173,   159,   194,   175,   174,   177,
     206,   197,   178,   176,   187,   184,   179,   180,   107,   191,
     196,   186,    77,   195,    80,    81,    83,    85,    88,    92,
      92,    92,    92,    92,   192,   199,    89,   221,   164,   222,
     107,   190,   128,    69,   198,    90,   201,   223,   133,   217,
     220,   224,   205,   225,   237,   245,   238,   239,   164,   241,
     249,   151,   151,   151,   117,   254,   159,   218,   219,   117,
     258,   256,   164,   164,   148,   118,   119,   193,   120,   164,
     118,   119,   259,   120,   141,   242,   260,   263,   162,   163,
     264,   265,   107,   266,   235,   267,   268,   269,   273,   158,
     272,   169,   137,    79,   234,    92,   130,   141,   158,     0,
     141,   141,   158,   141,   158,   141,   158,   164,   141,   204,
     158,     0,   141,     0,     0,     0,   164,     0,   257,   -48,
     244,   -48,    69,     0,     0,     0,   253,   243,    69,   -48,
     248,     0,     0,   -48,     0,   -48,     0,     0,     0,    88,
       0,     0,     0,     0,   207,     0,     0,     0,   141,     0,
       0,     0,     0,   216,     0,     0,   -48,     0,   -48,     0,
     -46,   157,   210,     0,   -46,     0,   -46,     0,   141,     0,
       0,     0,     0,     0,   -46,     0,    92,     0,   -46,   -46,
     -46,     0,   141,   141,   210,   210,   210,   210,   210,   141,
       0,   -53,     1,     0,     2,   -53,     3,   -53,     4,     5,
      70,   -46,     0,   -46,     0,   -53,     6,     7,     8,   -53,
     -53,   -53,     0,     0,     9,    10,     0,     0,    11,    12,
      13,   135,    15,     0,    16,     0,    17,   141,    18,     0,
      19,     0,   136,    21,    23,    23,   141,     0,    99,   100,
     101,     0,     0,   102,   103,   104,   105,   106,     0,    24,
       0,     0,     0,     0,    25,     0,     0,    26,    27,     0,
       0,    28,    29,    30,    31,    32,    33,    34,    35,    36,
       0,     0,     0,     0,    37,    38,   -34,     1,     0,     2,
       0,     3,     0,     4,     5,     0,     0,     0,     0,     0,
       0,     6,     7,     8,     0,     0,     0,     0,     0,     9,
      10,     0,     0,    11,    12,    13,    14,    15,     0,    16,
       0,    17,     0,    18,     0,    19,     0,    20,    21,    22,
      23,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,    24,     0,     0,     0,     0,    25,
       0,     0,    26,    27,     0,     0,    28,    29,    30,    31,
      32,    33,    34,    35,    36,     0,     0,     0,     0,    37,
      38,   154,     0,     2,   -34,     3,   -34,     4,     5,     0,
       0,     0,     0,     0,   -34,     6,     7,     8,   -34,     0,
     -34,     0,     0,     9,    10,     0,     0,    11,    12,    13,
      14,    15,     0,    16,     0,    17,     0,    18,     0,    19,
       0,    20,    21,    22,    23,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,    24,     0,
       0,     0,     0,    25,     0,     0,    26,    27,     0,     0,
      28,    29,    30,    31,    32,    33,    34,    35,    36,     0,
       0,     0,     0,    37,    38,   143,     0,     2,     0,     3,
       0,     4,     5,     0,     0,     0,     0,     0,     0,     6,
       7,     8,   -34,   -34,     0,     0,     0,     9,    10,     0,
       0,    11,    12,    13,    14,    15,     0,    16,     0,    17,
       0,    18,     0,    19,     0,    20,    21,    22,    23,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,    24,     0,     0,     0,     0,    25,     0,     0,
      26,    27,     0,     0,    28,    29,    30,    31,    32,    33,
      34,    35,    36,     0,     0,     0,     0,    37,    38,   145,
       0,     2,     0,     3,     0,     4,     5,     0,     0,     0,
       0,     0,     0,     6,     7,     8,   -34,   -34,     0,     0,
       0,     9,    10,     0,     0,    11,    12,    13,    14,    15,
       0,    16,     0,    17,     0,    18,     0,    19,     0,    20,
      21,    22,    23,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,    24,     0,     0,     0,
       0,    25,     0,     0,    26,    27,     0,     0,    28,    29,
      30,    31,    32,    33,    34,    35,    36,     0,     0,     0,
       0,    37,    38,    72,     0,     2,     0,     3,     0,     4,
       5,     0,     0,     0,     0,     0,     0,     6,     7,     8,
       0,   -34,     0,     0,     0,     9,    10,     0,     0,    11,
      12,    13,    14,    15,     0,    16,     0,    17,     0,    18,
       0,    19,     0,    20,    21,    22,    23,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
      24,     0,     0,     0,     0,    25,     0,     0,    26,    27,
       0,     0,    28,    29,    30,    31,    32,    33,    34,    35,
      36,     0,     0,     0,     0,    37,    38,     1,     0,     2,
       0,     3,     0,     4,     5,     0,     0,     0,     0,     0,
       0,     6,     7,     8,     0,   -34,     0,     0,     0,     9,
      10,     0,     0,    11,    12,    13,    14,    15,     0,    16,
       0,    17,     0,    18,     0,    19,     0,    20,    21,    22,
      23,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,    24,     0,     0,     0,     0,    25,
       0,     0,    26,    27,     0,     0,    28,    29,    30,    31,
      32,    33,    34,    35,    36,     0,     0,     0,     0,    37,
      38,   252,     0,     2,     0,     3,     0,     4,     5,     0,
       0,     0,     0,     0,     0,     6,     7,     8,     0,   -34,
       0,     0,     0,     9,    10,     0,     0,    11,    12,    13,
      14,    15,     0,    16,     0,    17,     0,    18,     0,    19,
       0,    20,    21,    22,    23,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,    24,     0,
       0,     0,     0,    25,     0,     0,    26,    27,     0,     0,
      28,    29,    30,    31,    32,    33,    34,    35,    36,     0,
       0,     0,     0,    37,    38,  -107,    76,     0,     2,  -107,
       3,  -107,     4,     5,     0,     0,     0,     0,     0,  -107,
       0,     0,     0,  -107,  -107,  -107,     0,     0,     0,     0,
    -107,  -107,     0,     0,     0,   170,    15,  -107,    16,  -107,
      17,  -107,    18,  -107,    19,  -107,   136,    21,  -107,    23,
       0,     0,     0,     0,     0,     0,     0,     0,     0,  -107,
      76,     0,     2,  -107,     3,  -107,     4,     5,    25,     0,
       0,    26,    27,  -107,     0,  -107,     0,  -107,  -107,  -107,
      33,    34,    35,    36,  -107,  -107,     0,     0,    37,     0,
      15,  -107,    16,  -107,    17,  -107,    18,  -107,    19,  -107,
      20,    21,    22,    23,     0,     0,     0,     0,     0,     0,
       0,     0,     0,  -105,    76,     0,     2,  -105,     3,  -105,
       4,     5,    25,     0,     0,    26,    27,  -105,     0,  -107,
       0,  -105,  -105,  -105,    33,    34,    35,    36,  -105,  -105,
       0,     0,    37,     0,    15,  -105,    16,  -105,    17,  -105,
      18,  -105,    19,  -105,    20,    21,    22,    23,     0,     0,
       0,     0,     0,     0,     0,     0,     0,   -54,    76,     0,
       2,   -54,     3,   -54,     4,     5,    25,     0,     0,    26,
      27,   -54,     0,  -105,     0,   -54,   -54,   -54,    33,    34,
      35,    36,     0,     0,     0,     0,    37,    87,    15,     0,
      16,     0,    17,     0,    18,     0,    19,     0,   205,    21,
       0,    23,     0,    23,     0,     0,   228,     0,     0,     0,
       0,     0,   229,   230,   231,   232,   233,     0,     0,     0,
      25,     0,     0,    26,    27,    26,    27,    28,    29,    30,
      31,    32,    33,    34,    35,    36,     0,     0,   -44,    76,
      37,     2,   -44,     3,   -44,     4,     5,     0,     0,     0,
       0,     0,   -44,     0,     0,     0,   -44,   -44,   -44,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,    15,
       0,    16,     0,    17,     0,    18,     0,    19,     0,   -44,
      21,   -44,    23,    23,   202,   203,     0,    99,   100,   101,
     182,     0,   102,   103,   104,   105,   106,     0,     0,     0,
       0,    25,     0,     0,    26,    27,     0,     0,     0,    29,
      30,    31,    32,    33,    34,    35,    36,     0,     0,   -38,
      76,    37,     2,   -38,     3,   -38,     4,     5,     0,     0,
       0,     0,     0,   -38,     0,     0,     0,   -38,   -38,   -38,
       0,     0,     0,     0,   138,   139,     0,     0,     0,     0,
      15,     0,    16,     0,    17,     0,    18,     0,    19,     0,
     -38,    21,   -38,    23,     0,     0,     0,     0,     0,     0,
       0,     0,     0,  -120,    76,     0,     2,  -120,     3,  -120,
       4,     5,    25,     0,     0,    26,    27,  -120,     0,   140,
       0,  -120,  -120,  -120,    33,    34,    35,    36,     0,     0,
       0,     0,    37,     0,    15,     0,    16,     0,    17,     0,
      18,     0,    19,     0,  -120,    21,  -120,    23,     0,     0,
       0,     0,     0,     0,     0,     0,     0,   -55,    76,     0,
       2,   -55,     3,   -55,     4,     5,    25,     0,     0,    26,
      27,   -55,     0,   147,     0,   -55,   -55,   -55,    33,    34,
      35,    36,     0,     0,     0,     0,    37,     0,    15,     0,
      16,     0,    17,     0,    18,     0,    19,     0,   -55,    21,
     -55,    23,     0,     0,     0,     0,     0,     0,     0,     0,
       0,  -129,    76,     0,     2,  -129,     3,  -129,     4,     5,
      25,     0,     0,    26,    27,  -129,     0,   140,     0,  -129,
    -129,  -129,    33,    34,    35,    36,     0,     0,     0,     0,
      37,     0,    15,     0,    16,     0,    17,     0,    18,     0,
      19,     0,  -129,    21,  -129,    23,     0,     0,     0,     0,
       0,     0,     0,     0,     0,  -130,    76,     0,     2,  -130,
       3,  -130,     4,     5,    25,     0,     0,    26,    27,  -130,
       0,  -129,     0,  -130,  -130,  -130,    33,    34,    35,    36,
       0,     0,     0,     0,    37,     0,    15,     0,    16,     0,
      17,     0,    18,     0,    19,     0,  -130,    21,  -130,    23,
       0,     0,     0,     0,     0,     0,     0,     0,     0,   -73,
      76,     0,     2,   -73,     3,   -73,     4,     5,    25,     0,
       0,    26,    27,   -73,     0,  -130,     0,   -73,   -73,   -73,
      33,    34,    35,    36,     0,     0,     0,     0,    37,     0,
      15,     0,    16,     0,    17,     0,    18,     0,    19,     0,
     -73,    21,   -73,    23,     0,     0,     0,     0,     0,     0,
     -63,    76,     0,     2,   -63,     3,   -63,     4,     5,     0,
       0,     0,    25,     0,   -63,    26,    27,     0,   -63,   -63,
     -63,     0,     0,     0,    33,    34,    35,    36,     0,     0,
       0,    15,    37,    16,     0,    17,     0,    18,     0,    19,
       0,   -63,    21,   -63,    23,     0,     0,     0,     0,     0,
       0,   -67,    76,     0,     2,   -67,     3,   -67,     4,     5,
       0,     0,     0,    25,     0,   -67,    26,    27,     0,   -67,
     -67,   -67,     0,     0,     0,    33,    34,    35,    36,     0,
       0,     0,    15,    37,    16,     0,    17,     0,    18,     0,
      19,     0,   -67,    21,   -67,    23,     0,     0,     0,     0,
       0,     0,   -59,    76,     0,     2,   -59,     3,   -59,     4,
       5,     0,     0,     0,    25,     0,   -59,    26,    27,     0,
     -59,   -59,   -59,     0,     0,     0,    33,    34,    35,    36,
       0,     0,     0,    15,    37,    16,     0,    17,     0,    18,
       0,    19,     0,   -59,    21,   -59,    23,     0,     0,     0,
       0,     0,     0,   -69,    76,     0,     2,   -69,     3,   -69,
       4,     5,     0,     0,     0,    25,     0,   -69,    26,    27,
       0,   -69,   -69,   -69,     0,     0,     0,    33,    34,    35,
      36,     0,     0,     0,    15,    37,    16,     0,    17,     0,
      18,     0,    19,     0,   -69,    21,   -69,    23,     0,     0,
       0,     0,     0,     0,   -68,    76,     0,     2,   -68,     3,
     -68,     4,     5,     0,     0,     0,    25,     0,   -68,    26,
      27,     0,   -68,   -68,   -68,     0,     0,     0,    33,    34,
      35,    36,     0,     0,     0,    15,    37,    16,     0,    17,
       0,    18,     0,    19,     0,   -68,    21,   -68,    23,     0,
       0,     0,     0,     0,     0,   -72,    76,     0,     2,   -72,
       3,   -72,     4,     5,     0,     0,     0,    25,     0,   -72,
      26,    27,     0,   -72,   -72,   -72,     0,     0,     0,    33,
      34,    35,    36,     0,     0,     0,    15,    37,    16,     0,
      17,     0,    18,     0,    19,     0,   -72,    21,   -72,    23,
       0,     0,     0,     0,     0,     0,   -80,    76,     0,     2,
     -80,     3,   -80,     4,     5,     0,     0,     0,    25,     0,
     -80,    26,    27,     0,   -80,   -80,   -80,     0,     0,     0,
      33,    34,    35,    36,     0,     0,     0,    15,    37,    16,
       0,    17,     0,    18,     0,    19,     0,   -80,    21,   -80,
      23,     0,     0,     0,     0,     0,     0,   -62,    76,     0,
       2,   -62,     3,   -62,     4,     5,     0,     0,     0,    25,
       0,   -62,    26,    27,     0,   -62,   -62,   -62,     0,     0,
       0,    33,    34,    35,    36,     0,     0,     0,    15,    37,
      16,     0,    17,     0,    18,     0,    19,     0,   -62,    21,
     -62,    23,     0,     0,     0,     0,     0,     0,   -66,    76,
       0,     2,   -66,     3,   -66,     4,     5,     0,     0,     0,
      25,     0,   -66,    26,    27,     0,   -66,   -66,   -66,     0,
       0,     0,    33,    34,    35,    36,     0,     0,     0,    15,
      37,    16,     0,    17,     0,    18,     0,    19,     0,   -66,
      21,   -66,    23,     0,     0,     0,     0,     0,     0,   -58,
      76,     0,     2,   -58,     3,   -58,     4,     5,     0,     0,
       0,    25,     0,   -58,    26,    27,     0,   -58,   -58,   -58,
       0,     0,     0,    33,    34,    35,    36,     0,     0,     0,
      15,    37,    16,     0,    17,     0,    18,     0,    19,     0,
     -58,    21,   -58,    23,     0,     0,     0,     0,     0,     0,
     -71,    76,     0,     2,   -71,     3,   -71,     4,     5,     0,
       0,     0,    25,     0,   -71,    26,    27,     0,   -71,   -71,
     -71,     0,     0,     0,    33,    34,    35,    36,     0,     0,
       0,    15,    37,    16,     0,    17,     0,    18,     0,    19,
       0,   -71,    21,   -71,    23,     0,     0,     0,     0,     0,
       0,   -70,    76,     0,     2,   -70,     3,   -70,     4,     5,
       0,     0,     0,    25,     0,   -70,    26,    27,     0,   -70,
     -70,   -70,     0,     0,     0,    33,    34,    35,    36,     0,
       0,     0,    15,    37,    16,     0,    17,     0,    18,     0,
      19,     0,   -70,    21,   -70,    23,     0,     0,     0,     0,
       0,     0,   -61,    76,     0,     2,   -61,     3,   -61,     4,
       5,     0,     0,     0,    25,     0,   -61,    26,    27,     0,
     -61,   -61,   -61,     0,     0,     0,    33,    34,    35,    36,
       0,     0,     0,    15,    37,    16,     0,    17,     0,    18,
       0,    19,     0,   -61,    21,   -61,     0,     0,     0,     0,
       0,     0,     0,   -65,    76,     0,     2,   -65,     3,   -65,
       4,     5,     0,     0,     0,    25,     0,   -65,    26,    27,
       0,   -65,   -65,   -65,     0,     0,     0,    33,    34,    35,
      36,     0,     0,     0,    15,    37,    16,     0,    17,     0,
      18,     0,    19,     0,   -65,    21,   -65,     0,     0,     0,
       0,     0,     0,     0,   -57,    76,     0,     2,   -57,     3,
     -57,     4,     5,     0,     0,     0,    25,     0,   -57,    26,
      27,     0,   -57,   -57,   -57,     0,     0,     0,    33,    34,
      35,    36,     0,     0,     0,    15,    37,    16,     0,    17,
       0,    18,     0,    19,     0,   -57,    21,   -57,     0,     0,
       0,     0,     0,     0,     0,   -79,    76,     0,     2,   -79,
       3,   -79,     4,     5,     0,     0,     0,    25,     0,   -79,
      26,    27,     0,   -79,   -79,   -79,     0,     0,     0,    33,
      34,    35,    36,     0,     0,     0,    15,    37,    16,     0,
      17,     0,    18,     0,    19,     0,   -79,    21,   -79,     0,
       0,     0,     0,     0,     0,     0,   -60,    76,     0,     2,
     -60,     3,   -60,     4,     5,     0,     0,     0,    25,     0,
     -60,    26,    27,     0,   -60,   -60,   -60,     0,     0,     0,
      33,    34,    35,    36,     0,     0,     0,    15,    37,    16,
       0,    17,     0,    18,     0,    19,     0,   -60,    21,   -60,
       0,     0,     0,     0,     0,     0,     0,   -64,    76,     0,
       2,   -64,     3,   -64,     4,     5,     0,     0,     0,    25,
       0,   -64,    26,    27,     0,   -64,   -64,   -64,     0,     0,
       0,    33,    34,    35,    36,     0,     0,     0,    15,    37,
      16,     0,    17,     0,    18,     0,    19,     0,   -64,    21,
     -64,     0,     0,     0,     0,     0,     0,     0,   -56,    76,
       0,     2,   -56,     3,   -56,     4,     5,     0,     0,     0,
      25,     0,   -56,    26,    27,     0,   -56,   -56,   -56,     0,
       0,     0,    33,    34,    35,    36,     0,     0,     0,    15,
      37,    16,     0,    17,     0,    18,     0,    19,     0,   -56,
      21,   -56,     0,     0,     0,     0,     0,     0,    76,     0,
       2,     0,     3,     0,     4,     5,     0,     0,     0,     0,
       0,    25,     0,     0,    26,    27,     0,     0,     0,     0,
       0,     0,     0,    33,    34,    35,    36,    87,    15,     0,
      16,    37,    17,     0,    18,     0,    19,     0,     0,    21,
       0,    23,     0,     0,     0,     0,     0,    76,     0,     2,
       0,     3,     0,     4,     5,     0,     0,     0,     0,     0,
      25,     0,     0,    26,    27,     0,     0,    28,    29,    30,
      31,    32,    33,    34,    35,    36,     0,    15,     0,    16,
      37,    17,     0,    18,     0,    19,     0,     0,    21,     0,
      23,     0,     0,     0,     0,     0,    76,     0,     2,     0,
       3,     0,     4,     5,     0,     0,     0,     0,     0,    25,
       0,     0,    26,    27,     0,     0,   127,    29,    30,    31,
      32,    33,    34,    35,    36,     0,    15,     0,    16,    37,
      17,     0,    18,     0,    19,     0,     0,    21,     0,    23,
       0,     0,     0,     0,     0,    76,     0,     2,     0,     3,
       0,     4,     5,     0,     0,     0,     0,     0,    25,     0,
       0,    26,    27,     0,     0,     0,    29,    30,    31,    32,
      33,    34,    35,    36,     0,    15,     0,    16,    37,    17,
       0,    18,     0,    19,     0,     0,    21,     0,    23,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,    76,
       0,     2,     0,     3,     0,     4,     5,    25,     0,     0,
      26,    27,     0,     0,   200,     0,     0,     0,     0,    33,
      34,    35,    36,   208,   209,     0,     0,    37,     0,    15,
       0,    16,     0,    17,     0,    18,     0,    19,     0,     0,
      21,     0,     0,     0,     0,     0,     0,     0,    76,     0,
       2,     0,     3,     0,     4,     5,     0,     0,     0,     0,
       0,    25,     0,     0,    26,    27,     0,     0,     0,     0,
       0,     0,     0,    33,    34,    35,    36,     0,    15,     0,
      16,    37,    17,     0,    18,     0,    19,     0,     0,    21,
       0,    23,     0,     0,     0,     0,     0,    76,     0,     2,
       0,     3,     0,     4,     5,     0,     0,     0,     0,     0,
      25,     0,     0,    26,    27,     0,     0,   215,     0,     0,
       0,     0,    33,    34,    35,    36,     0,    15,     0,    16,
      37,    17,     0,    18,     0,    19,     0,     0,    21,     0,
      23,     0,     0,     0,     0,     0,    76,     0,     2,     0,
       3,     0,     4,     5,     0,     0,     0,     0,     0,    25,
       0,     0,    26,    27,     0,     0,   140,     0,     0,     0,
       0,    33,    34,    35,    36,     0,    15,     0,    16,    37,
      17,     0,    18,     0,    19,     0,     0,    21,     0,    23,
       0,     0,     0,     0,     0,    76,     0,     2,     0,     3,
       0,     4,     5,     0,     0,     0,     0,     0,    25,     0,
       0,    26,    27,     0,     0,     0,     0,     0,     0,     0,
      33,    34,    35,    36,     0,    15,     0,    16,    37,    17,
       0,    18,     0,    19,     0,     0,    21,  -116,  -116,  -116,
     -48,   -48,     0,     0,     0,  -116,  -116,     0,     0,  -116,
    -116,  -116,  -116,     0,     0,     0,     0,    25,     0,     0,
      26,    27,     0,   -48,     0,   -48,     0,     0,     0,    33,
      34,    35,    36,     0,     0,     0,     0,    37,    23,   181,
    -116,     0,    99,   100,   101,   182,     0,   102,   103,   104,
     105,   106,     0,  -116,  -116,  -116,  -116,     0,     0,     0,
    -119,  -119,  -119,   -48,   -48,     0,  -116,    70,  -119,  -119,
       0,     0,  -119,  -119,  -119,  -119,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,   -48,     0,   -48,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,  -119,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,  -119,  -119,  -119,  -119,
       0,     0,     0,     0,     0,     0,     0,     0,     0,  -119,
      70
};

static const yytype_int16 yycheck[] =
{
       0,     3,    85,     3,    27,    14,    43,    19,     2,    44,
      91,    11,    12,    13,    14,   108,    15,    16,    17,    18,
      19,    42,    44,    23,    24,    60,    61,   185,    28,    41,
      44,    43,   190,    28,    23,    24,    36,   130,    16,    17,
      18,    19,    18,    19,    43,    45,    64,    61,     0,    71,
      72,    73,    74,    83,    54,    57,    58,    57,    58,    41,
      70,    43,    62,    83,    66,    42,    66,    62,    19,    69,
      18,    19,    66,    85,    69,    12,    13,    77,    87,   237,
      80,    81,    70,    83,    70,    85,    19,    87,    88,   182,
      90,   172,    92,    92,    32,    90,   119,    36,    34,    40,
     137,   124,    56,    38,    62,    52,    56,    56,   108,    65,
      69,   111,     8,    68,    10,    11,    12,    13,    14,    15,
      16,    17,    18,    19,    64,    69,   135,     4,   128,     6,
     130,    61,    28,   133,    80,   135,    70,    14,   137,    70,
      19,    18,    41,    20,    61,     9,    59,    62,   148,    81,
      21,   151,   152,   153,    68,    59,   151,   152,   153,    68,
      81,    59,   162,   163,    60,    79,    80,    81,    82,   169,
      79,    80,    19,    82,    54,   198,    19,     9,    74,    75,
      19,    22,   182,    21,   184,    19,    59,    10,    10,    69,
      11,    87,    45,     9,   184,    91,    36,    77,    78,    -1,
      80,    81,    82,    83,    84,    85,    86,   207,    88,   133,
      90,    -1,    92,    -1,    -1,    -1,   216,    -1,   241,     4,
     222,     6,   222,    -1,    -1,    -1,   228,   221,   228,    14,
     224,    -1,    -1,    18,    -1,    20,    -1,    -1,    -1,   135,
      -1,    -1,    -1,    -1,   140,    -1,    -1,    -1,   128,    -1,
      -1,    -1,    -1,   149,    -1,    -1,    41,    -1,    43,    -1,
       0,     1,   142,    -1,     4,    -1,     6,    -1,   148,    -1,
      -1,    -1,    -1,    -1,    14,    -1,   172,    -1,    18,    19,
      20,    -1,   162,   163,   164,   165,   166,   167,   168,   169,
      -1,     0,     1,    -1,     3,     4,     5,     6,     7,     8,
      85,    41,    -1,    43,    -1,    14,    15,    16,    17,    18,
      19,    20,    -1,    -1,    23,    24,    -1,    -1,    27,    28,
      29,    30,    31,    -1,    33,    -1,    35,   207,    37,    -1,
      39,    -1,    41,    42,    44,    44,   216,    -1,    48,    49,
      50,    -1,    -1,    53,    54,    55,    56,    57,    -1,    58,
      -1,    -1,    -1,    -1,    63,    -1,    -1,    66,    67,    -1,
      -1,    70,    71,    72,    73,    74,    75,    76,    77,    78,
      -1,    -1,    -1,    -1,    83,    84,     0,     1,    -1,     3,
      -1,     5,    -1,     7,     8,    -1,    -1,    -1,    -1,    -1,
      -1,    15,    16,    17,    -1,    -1,    -1,    -1,    -1,    23,
      24,    -1,    -1,    27,    28,    29,    30,    31,    -1,    33,
      -1,    35,    -1,    37,    -1,    39,    -1,    41,    42,    43,
      44,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    58,    -1,    -1,    -1,    -1,    63,
      -1,    -1,    66,    67,    -1,    -1,    70,    71,    72,    73,
      74,    75,    76,    77,    78,    -1,    -1,    -1,    -1,    83,
      84,     1,    -1,     3,     4,     5,     6,     7,     8,    -1,
      -1,    -1,    -1,    -1,    14,    15,    16,    17,    18,    -1,
      20,    -1,    -1,    23,    24,    -1,    -1,    27,    28,    29,
      30,    31,    -1,    33,    -1,    35,    -1,    37,    -1,    39,
      -1,    41,    42,    43,    44,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    58,    -1,
      -1,    -1,    -1,    63,    -1,    -1,    66,    67,    -1,    -1,
      70,    71,    72,    73,    74,    75,    76,    77,    78,    -1,
      -1,    -1,    -1,    83,    84,     1,    -1,     3,    -1,     5,
      -1,     7,     8,    -1,    -1,    -1,    -1,    -1,    -1,    15,
      16,    17,    18,    19,    -1,    -1,    -1,    23,    24,    -1,
      -1,    27,    28,    29,    30,    31,    -1,    33,    -1,    35,
      -1,    37,    -1,    39,    -1,    41,    42,    43,    44,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    58,    -1,    -1,    -1,    -1,    63,    -1,    -1,
      66,    67,    -1,    -1,    70,    71,    72,    73,    74,    75,
      76,    77,    78,    -1,    -1,    -1,    -1,    83,    84,     1,
      -1,     3,    -1,     5,    -1,     7,     8,    -1,    -1,    -1,
      -1,    -1,    -1,    15,    16,    17,    18,    19,    -1,    -1,
      -1,    23,    24,    -1,    -1,    27,    28,    29,    30,    31,
      -1,    33,    -1,    35,    -1,    37,    -1,    39,    -1,    41,
      42,    43,    44,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    58,    -1,    -1,    -1,
      -1,    63,    -1,    -1,    66,    67,    -1,    -1,    70,    71,
      72,    73,    74,    75,    76,    77,    78,    -1,    -1,    -1,
      -1,    83,    84,     1,    -1,     3,    -1,     5,    -1,     7,
       8,    -1,    -1,    -1,    -1,    -1,    -1,    15,    16,    17,
      -1,    19,    -1,    -1,    -1,    23,    24,    -1,    -1,    27,
      28,    29,    30,    31,    -1,    33,    -1,    35,    -1,    37,
      -1,    39,    -1,    41,    42,    43,    44,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      58,    -1,    -1,    -1,    -1,    63,    -1,    -1,    66,    67,
      -1,    -1,    70,    71,    72,    73,    74,    75,    76,    77,
      78,    -1,    -1,    -1,    -1,    83,    84,     1,    -1,     3,
      -1,     5,    -1,     7,     8,    -1,    -1,    -1,    -1,    -1,
      -1,    15,    16,    17,    -1,    19,    -1,    -1,    -1,    23,
      24,    -1,    -1,    27,    28,    29,    30,    31,    -1,    33,
      -1,    35,    -1,    37,    -1,    39,    -1,    41,    42,    43,
      44,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    58,    -1,    -1,    -1,    -1,    63,
      -1,    -1,    66,    67,    -1,    -1,    70,    71,    72,    73,
      74,    75,    76,    77,    78,    -1,    -1,    -1,    -1,    83,
      84,     1,    -1,     3,    -1,     5,    -1,     7,     8,    -1,
      -1,    -1,    -1,    -1,    -1,    15,    16,    17,    -1,    19,
      -1,    -1,    -1,    23,    24,    -1,    -1,    27,    28,    29,
      30,    31,    -1,    33,    -1,    35,    -1,    37,    -1,    39,
      -1,    41,    42,    43,    44,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    58,    -1,
      -1,    -1,    -1,    63,    -1,    -1,    66,    67,    -1,    -1,
      70,    71,    72,    73,    74,    75,    76,    77,    78,    -1,
      -1,    -1,    -1,    83,    84,     0,     1,    -1,     3,     4,
       5,     6,     7,     8,    -1,    -1,    -1,    -1,    -1,    14,
      -1,    -1,    -1,    18,    19,    20,    -1,    -1,    -1,    -1,
      25,    26,    -1,    -1,    -1,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,     0,
       1,    -1,     3,     4,     5,     6,     7,     8,    63,    -1,
      -1,    66,    67,    14,    -1,    70,    -1,    18,    19,    20,
      75,    76,    77,    78,    25,    26,    -1,    -1,    83,    -1,
      31,    32,    33,    34,    35,    36,    37,    38,    39,    40,
      41,    42,    43,    44,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,     0,     1,    -1,     3,     4,     5,     6,
       7,     8,    63,    -1,    -1,    66,    67,    14,    -1,    70,
      -1,    18,    19,    20,    75,    76,    77,    78,    25,    26,
      -1,    -1,    83,    -1,    31,    32,    33,    34,    35,    36,
      37,    38,    39,    40,    41,    42,    43,    44,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,     0,     1,    -1,
       3,     4,     5,     6,     7,     8,    63,    -1,    -1,    66,
      67,    14,    -1,    70,    -1,    18,    19,    20,    75,    76,
      77,    78,    -1,    -1,    -1,    -1,    83,    30,    31,    -1,
      33,    -1,    35,    -1,    37,    -1,    39,    -1,    41,    42,
      -1,    44,    -1,    44,    -1,    -1,    47,    -1,    -1,    -1,
      -1,    -1,    53,    54,    55,    56,    57,    -1,    -1,    -1,
      63,    -1,    -1,    66,    67,    66,    67,    70,    71,    72,
      73,    74,    75,    76,    77,    78,    -1,    -1,     0,     1,
      83,     3,     4,     5,     6,     7,     8,    -1,    -1,    -1,
      -1,    -1,    14,    -1,    -1,    -1,    18,    19,    20,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    31,
      -1,    33,    -1,    35,    -1,    37,    -1,    39,    -1,    41,
      42,    43,    44,    44,    45,    46,    -1,    48,    49,    50,
      51,    -1,    53,    54,    55,    56,    57,    -1,    -1,    -1,
      -1,    63,    -1,    -1,    66,    67,    -1,    -1,    -1,    71,
      72,    73,    74,    75,    76,    77,    78,    -1,    -1,     0,
       1,    83,     3,     4,     5,     6,     7,     8,    -1,    -1,
      -1,    -1,    -1,    14,    -1,    -1,    -1,    18,    19,    20,
      -1,    -1,    -1,    -1,    25,    26,    -1,    -1,    -1,    -1,
      31,    -1,    33,    -1,    35,    -1,    37,    -1,    39,    -1,
      41,    42,    43,    44,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,     0,     1,    -1,     3,     4,     5,     6,
       7,     8,    63,    -1,    -1,    66,    67,    14,    -1,    70,
      -1,    18,    19,    20,    75,    76,    77,    78,    -1,    -1,
      -1,    -1,    83,    -1,    31,    -1,    33,    -1,    35,    -1,
      37,    -1,    39,    -1,    41,    42,    43,    44,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,     0,     1,    -1,
       3,     4,     5,     6,     7,     8,    63,    -1,    -1,    66,
      67,    14,    -1,    70,    -1,    18,    19,    20,    75,    76,
      77,    78,    -1,    -1,    -1,    -1,    83,    -1,    31,    -1,
      33,    -1,    35,    -1,    37,    -1,    39,    -1,    41,    42,
      43,    44,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,     0,     1,    -1,     3,     4,     5,     6,     7,     8,
      63,    -1,    -1,    66,    67,    14,    -1,    70,    -1,    18,
      19,    20,    75,    76,    77,    78,    -1,    -1,    -1,    -1,
      83,    -1,    31,    -1,    33,    -1,    35,    -1,    37,    -1,
      39,    -1,    41,    42,    43,    44,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,     0,     1,    -1,     3,     4,
       5,     6,     7,     8,    63,    -1,    -1,    66,    67,    14,
      -1,    70,    -1,    18,    19,    20,    75,    76,    77,    78,
      -1,    -1,    -1,    -1,    83,    -1,    31,    -1,    33,    -1,
      35,    -1,    37,    -1,    39,    -1,    41,    42,    43,    44,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,     0,
       1,    -1,     3,     4,     5,     6,     7,     8,    63,    -1,
      -1,    66,    67,    14,    -1,    70,    -1,    18,    19,    20,
      75,    76,    77,    78,    -1,    -1,    -1,    -1,    83,    -1,
      31,    -1,    33,    -1,    35,    -1,    37,    -1,    39,    -1,
      41,    42,    43,    44,    -1,    -1,    -1,    -1,    -1,    -1,
       0,     1,    -1,     3,     4,     5,     6,     7,     8,    -1,
      -1,    -1,    63,    -1,    14,    66,    67,    -1,    18,    19,
      20,    -1,    -1,    -1,    75,    76,    77,    78,    -1,    -1,
      -1,    31,    83,    33,    -1,    35,    -1,    37,    -1,    39,
      -1,    41,    42,    43,    44,    -1,    -1,    -1,    -1,    -1,
      -1,     0,     1,    -1,     3,     4,     5,     6,     7,     8,
      -1,    -1,    -1,    63,    -1,    14,    66,    67,    -1,    18,
      19,    20,    -1,    -1,    -1,    75,    76,    77,    78,    -1,
      -1,    -1,    31,    83,    33,    -1,    35,    -1,    37,    -1,
      39,    -1,    41,    42,    43,    44,    -1,    -1,    -1,    -1,
      -1,    -1,     0,     1,    -1,     3,     4,     5,     6,     7,
       8,    -1,    -1,    -1,    63,    -1,    14,    66,    67,    -1,
      18,    19,    20,    -1,    -1,    -1,    75,    76,    77,    78,
      -1,    -1,    -1,    31,    83,    33,    -1,    35,    -1,    37,
      -1,    39,    -1,    41,    42,    43,    44,    -1,    -1,    -1,
      -1,    -1,    -1,     0,     1,    -1,     3,     4,     5,     6,
       7,     8,    -1,    -1,    -1,    63,    -1,    14,    66,    67,
      -1,    18,    19,    20,    -1,    -1,    -1,    75,    76,    77,
      78,    -1,    -1,    -1,    31,    83,    33,    -1,    35,    -1,
      37,    -1,    39,    -1,    41,    42,    43,    44,    -1,    -1,
      -1,    -1,    -1,    -1,     0,     1,    -1,     3,     4,     5,
       6,     7,     8,    -1,    -1,    -1,    63,    -1,    14,    66,
      67,    -1,    18,    19,    20,    -1,    -1,    -1,    75,    76,
      77,    78,    -1,    -1,    -1,    31,    83,    33,    -1,    35,
      -1,    37,    -1,    39,    -1,    41,    42,    43,    44,    -1,
      -1,    -1,    -1,    -1,    -1,     0,     1,    -1,     3,     4,
       5,     6,     7,     8,    -1,    -1,    -1,    63,    -1,    14,
      66,    67,    -1,    18,    19,    20,    -1,    -1,    -1,    75,
      76,    77,    78,    -1,    -1,    -1,    31,    83,    33,    -1,
      35,    -1,    37,    -1,    39,    -1,    41,    42,    43,    44,
      -1,    -1,    -1,    -1,    -1,    -1,     0,     1,    -1,     3,
       4,     5,     6,     7,     8,    -1,    -1,    -1,    63,    -1,
      14,    66,    67,    -1,    18,    19,    20,    -1,    -1,    -1,
      75,    76,    77,    78,    -1,    -1,    -1,    31,    83,    33,
      -1,    35,    -1,    37,    -1,    39,    -1,    41,    42,    43,
      44,    -1,    -1,    -1,    -1,    -1,    -1,     0,     1,    -1,
       3,     4,     5,     6,     7,     8,    -1,    -1,    -1,    63,
      -1,    14,    66,    67,    -1,    18,    19,    20,    -1,    -1,
      -1,    75,    76,    77,    78,    -1,    -1,    -1,    31,    83,
      33,    -1,    35,    -1,    37,    -1,    39,    -1,    41,    42,
      43,    44,    -1,    -1,    -1,    -1,    -1,    -1,     0,     1,
      -1,     3,     4,     5,     6,     7,     8,    -1,    -1,    -1,
      63,    -1,    14,    66,    67,    -1,    18,    19,    20,    -1,
      -1,    -1,    75,    76,    77,    78,    -1,    -1,    -1,    31,
      83,    33,    -1,    35,    -1,    37,    -1,    39,    -1,    41,
      42,    43,    44,    -1,    -1,    -1,    -1,    -1,    -1,     0,
       1,    -1,     3,     4,     5,     6,     7,     8,    -1,    -1,
      -1,    63,    -1,    14,    66,    67,    -1,    18,    19,    20,
      -1,    -1,    -1,    75,    76,    77,    78,    -1,    -1,    -1,
      31,    83,    33,    -1,    35,    -1,    37,    -1,    39,    -1,
      41,    42,    43,    44,    -1,    -1,    -1,    -1,    -1,    -1,
       0,     1,    -1,     3,     4,     5,     6,     7,     8,    -1,
      -1,    -1,    63,    -1,    14,    66,    67,    -1,    18,    19,
      20,    -1,    -1,    -1,    75,    76,    77,    78,    -1,    -1,
      -1,    31,    83,    33,    -1,    35,    -1,    37,    -1,    39,
      -1,    41,    42,    43,    44,    -1,    -1,    -1,    -1,    -1,
      -1,     0,     1,    -1,     3,     4,     5,     6,     7,     8,
      -1,    -1,    -1,    63,    -1,    14,    66,    67,    -1,    18,
      19,    20,    -1,    -1,    -1,    75,    76,    77,    78,    -1,
      -1,    -1,    31,    83,    33,    -1,    35,    -1,    37,    -1,
      39,    -1,    41,    42,    43,    44,    -1,    -1,    -1,    -1,
      -1,    -1,     0,     1,    -1,     3,     4,     5,     6,     7,
       8,    -1,    -1,    -1,    63,    -1,    14,    66,    67,    -1,
      18,    19,    20,    -1,    -1,    -1,    75,    76,    77,    78,
      -1,    -1,    -1,    31,    83,    33,    -1,    35,    -1,    37,
      -1,    39,    -1,    41,    42,    43,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,     0,     1,    -1,     3,     4,     5,     6,
       7,     8,    -1,    -1,    -1,    63,    -1,    14,    66,    67,
      -1,    18,    19,    20,    -1,    -1,    -1,    75,    76,    77,
      78,    -1,    -1,    -1,    31,    83,    33,    -1,    35,    -1,
      37,    -1,    39,    -1,    41,    42,    43,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,     0,     1,    -1,     3,     4,     5,
       6,     7,     8,    -1,    -1,    -1,    63,    -1,    14,    66,
      67,    -1,    18,    19,    20,    -1,    -1,    -1,    75,    76,
      77,    78,    -1,    -1,    -1,    31,    83,    33,    -1,    35,
      -1,    37,    -1,    39,    -1,    41,    42,    43,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,     0,     1,    -1,     3,     4,
       5,     6,     7,     8,    -1,    -1,    -1,    63,    -1,    14,
      66,    67,    -1,    18,    19,    20,    -1,    -1,    -1,    75,
      76,    77,    78,    -1,    -1,    -1,    31,    83,    33,    -1,
      35,    -1,    37,    -1,    39,    -1,    41,    42,    43,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,     0,     1,    -1,     3,
       4,     5,     6,     7,     8,    -1,    -1,    -1,    63,    -1,
      14,    66,    67,    -1,    18,    19,    20,    -1,    -1,    -1,
      75,    76,    77,    78,    -1,    -1,    -1,    31,    83,    33,
      -1,    35,    -1,    37,    -1,    39,    -1,    41,    42,    43,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,     0,     1,    -1,
       3,     4,     5,     6,     7,     8,    -1,    -1,    -1,    63,
      -1,    14,    66,    67,    -1,    18,    19,    20,    -1,    -1,
      -1,    75,    76,    77,    78,    -1,    -1,    -1,    31,    83,
      33,    -1,    35,    -1,    37,    -1,    39,    -1,    41,    42,
      43,    -1,    -1,    -1,    -1,    -1,    -1,    -1,     0,     1,
      -1,     3,     4,     5,     6,     7,     8,    -1,    -1,    -1,
      63,    -1,    14,    66,    67,    -1,    18,    19,    20,    -1,
      -1,    -1,    75,    76,    77,    78,    -1,    -1,    -1,    31,
      83,    33,    -1,    35,    -1,    37,    -1,    39,    -1,    41,
      42,    43,    -1,    -1,    -1,    -1,    -1,    -1,     1,    -1,
       3,    -1,     5,    -1,     7,     8,    -1,    -1,    -1,    -1,
      -1,    63,    -1,    -1,    66,    67,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    75,    76,    77,    78,    30,    31,    -1,
      33,    83,    35,    -1,    37,    -1,    39,    -1,    -1,    42,
      -1,    44,    -1,    -1,    -1,    -1,    -1,     1,    -1,     3,
      -1,     5,    -1,     7,     8,    -1,    -1,    -1,    -1,    -1,
      63,    -1,    -1,    66,    67,    -1,    -1,    70,    71,    72,
      73,    74,    75,    76,    77,    78,    -1,    31,    -1,    33,
      83,    35,    -1,    37,    -1,    39,    -1,    -1,    42,    -1,
      44,    -1,    -1,    -1,    -1,    -1,     1,    -1,     3,    -1,
       5,    -1,     7,     8,    -1,    -1,    -1,    -1,    -1,    63,
      -1,    -1,    66,    67,    -1,    -1,    70,    71,    72,    73,
      74,    75,    76,    77,    78,    -1,    31,    -1,    33,    83,
      35,    -1,    37,    -1,    39,    -1,    -1,    42,    -1,    44,
      -1,    -1,    -1,    -1,    -1,     1,    -1,     3,    -1,     5,
      -1,     7,     8,    -1,    -1,    -1,    -1,    -1,    63,    -1,
      -1,    66,    67,    -1,    -1,    -1,    71,    72,    73,    74,
      75,    76,    77,    78,    -1,    31,    -1,    33,    83,    35,
      -1,    37,    -1,    39,    -1,    -1,    42,    -1,    44,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,     1,
      -1,     3,    -1,     5,    -1,     7,     8,    63,    -1,    -1,
      66,    67,    -1,    -1,    70,    -1,    -1,    -1,    -1,    75,
      76,    77,    78,    25,    26,    -1,    -1,    83,    -1,    31,
      -1,    33,    -1,    35,    -1,    37,    -1,    39,    -1,    -1,
      42,    -1,    -1,    -1,    -1,    -1,    -1,    -1,     1,    -1,
       3,    -1,     5,    -1,     7,     8,    -1,    -1,    -1,    -1,
      -1,    63,    -1,    -1,    66,    67,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    75,    76,    77,    78,    -1,    31,    -1,
      33,    83,    35,    -1,    37,    -1,    39,    -1,    -1,    42,
      -1,    44,    -1,    -1,    -1,    -1,    -1,     1,    -1,     3,
      -1,     5,    -1,     7,     8,    -1,    -1,    -1,    -1,    -1,
      63,    -1,    -1,    66,    67,    -1,    -1,    70,    -1,    -1,
      -1,    -1,    75,    76,    77,    78,    -1,    31,    -1,    33,
      83,    35,    -1,    37,    -1,    39,    -1,    -1,    42,    -1,
      44,    -1,    -1,    -1,    -1,    -1,     1,    -1,     3,    -1,
       5,    -1,     7,     8,    -1,    -1,    -1,    -1,    -1,    63,
      -1,    -1,    66,    67,    -1,    -1,    70,    -1,    -1,    -1,
      -1,    75,    76,    77,    78,    -1,    31,    -1,    33,    83,
      35,    -1,    37,    -1,    39,    -1,    -1,    42,    -1,    44,
      -1,    -1,    -1,    -1,    -1,     1,    -1,     3,    -1,     5,
      -1,     7,     8,    -1,    -1,    -1,    -1,    -1,    63,    -1,
      -1,    66,    67,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      75,    76,    77,    78,    -1,    31,    -1,    33,    83,    35,
      -1,    37,    -1,    39,    -1,    -1,    42,    15,    16,    17,
      18,    19,    -1,    -1,    -1,    23,    24,    -1,    -1,    27,
      28,    29,    30,    -1,    -1,    -1,    -1,    63,    -1,    -1,
      66,    67,    -1,    41,    -1,    43,    -1,    -1,    -1,    75,
      76,    77,    78,    -1,    -1,    -1,    -1,    83,    44,    45,
      58,    -1,    48,    49,    50,    51,    -1,    53,    54,    55,
      56,    57,    -1,    71,    72,    73,    74,    -1,    -1,    -1,
      15,    16,    17,    18,    19,    -1,    84,    85,    23,    24,
      -1,    -1,    27,    28,    29,    30,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    41,    -1,    43,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    58,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    71,    72,    73,    74,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    84,
      85
};

  /* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
     symbol of state STATE-NUM.  */
static const yytype_uint8 yystos[] =
{
       0,     1,     3,     5,     7,     8,    15,    16,    17,    23,
      24,    27,    28,    29,    30,    31,    33,    35,    37,    39,
      41,    42,    43,    44,    58,    63,    66,    67,    70,    71,
      72,    73,    74,    75,    76,    77,    78,    83,    84,    87,
      88,   101,   102,   103,   104,   105,   106,   107,   108,   109,
     110,   111,   112,   113,   114,   115,   118,   119,   120,   121,
     122,   123,   124,   125,   126,   127,   128,   129,   133,   134,
      85,    87,     1,   102,    83,    83,     1,   114,   134,   113,
     114,   114,   134,   114,   134,   114,   134,    30,   114,   121,
     134,   105,   114,   116,   117,   116,   116,   116,   116,    48,
      49,    50,    53,    54,    55,    56,    57,   134,   135,   136,
     137,    60,    61,   134,    64,    93,    94,    68,    79,    80,
      82,    89,    90,   130,   131,   132,   130,    70,   114,   126,
     135,    42,     0,   105,   106,    30,    41,   103,    25,    26,
      70,   115,   134,     1,   102,     1,   102,    70,   114,    70,
     126,   134,    70,    70,     1,    87,   102,     1,   115,   126,
      19,    19,   114,   114,   134,   134,   134,   134,   134,   114,
      30,   117,   105,    32,    34,    36,    38,    40,    56,    56,
      56,    45,    51,   136,    52,    61,   134,    62,    99,   100,
      61,    65,    64,    81,   130,    68,    69,   130,    80,    69,
      70,    70,    45,    46,   104,    41,   106,   114,    25,    26,
     115,    18,    19,    18,    19,    70,   114,    70,   126,   126,
      19,     4,     6,    14,    18,    20,   117,   136,    47,    53,
      54,    55,    56,    57,   129,   134,    99,    61,    59,    62,
      99,    81,   130,    87,   102,     9,    95,    96,    87,    21,
      91,    92,     1,   102,    59,    99,    59,   130,    81,    19,
      19,    12,    13,     9,    19,    22,    21,    19,    59,    10,
      97,    98,    11,    10
};

  /* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_uint8 yyr1[] =
{
       0,    86,    87,    88,    88,    89,    90,    90,    91,    92,
      92,    92,    93,    94,    94,    94,    95,    96,    96,    96,
      97,    98,    98,    98,    99,   100,   100,   100,   101,   102,
     102,   102,   102,   102,   102,   103,   103,   104,   104,   104,
     104,   104,   104,   104,   104,   104,   104,   104,   104,   105,
     105,   105,   105,   106,   106,   107,   108,   108,   108,   108,
     109,   109,   109,   109,   110,   110,   110,   110,   111,   111,
     111,   111,   111,   111,   112,   112,   112,   112,   112,   113,
     113,   113,   114,   114,   114,   114,   115,   115,   115,   115,
     115,   115,   115,   115,   115,   115,   115,   115,   115,   115,
     115,   115,   115,   116,   116,   117,   117,   117,   118,   118,
     118,   118,   118,   118,   119,   119,   119,   120,   120,   120,
     121,   121,   121,   121,   121,   122,   122,   122,   122,   123,
     123,   124,   124,   125,   125,   126,   126,   126,   126,   126,
     127,   127,   127,   127,   127,   127,   127,   127,   127,   127,
     127,   127,   128,   128,   129,   129,   130,   130,   130,   130,
     131,   131,   131,   131,   132,   132,   133,   133,   133,   133,
     133,   134,   135,   135,   135,   135,   136,   136,   136,   136,
     136,   136,   136,   136,   136,   136,   136,   136,   136,   136,
     136,   136,   136,   137,   137
};

  /* YYR2[YYN] -- Number of symbols on the right hand side of rule YYN.  */
static const yytype_uint8 yyr2[] =
{
       0,     2,     1,     1,     2,     1,     1,     2,     1,     1,
       2,     0,     1,     1,     2,     0,     1,     1,     2,     0,
       1,     1,     2,     0,     1,     1,     2,     0,     1,     1,
       2,     3,     2,     1,     0,     1,     3,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     2,     3,     1,     2,     2,     3,     2,     2,     1,
       3,     2,     2,     1,     3,     2,     2,     1,     2,     2,
       3,     3,     2,     1,     1,     3,     3,     2,     2,     3,
       2,     2,     1,     2,     2,     3,     1,     3,     3,     3,
       3,     3,     1,     3,     1,     1,     1,     2,     2,     2,
       2,     2,     2,     1,     2,     1,     3,     0,     1,     3,
       3,     3,     2,     2,     3,     3,     2,     1,     3,     2,
       1,     1,     1,     1,     2,     3,     3,     2,     2,     3,
       3,     3,     3,     3,     3,     1,     1,     1,     1,     2,
       5,     7,     5,     3,     1,     3,     3,     5,     5,     5,
       2,     2,     1,     1,     3,     3,     1,     2,     3,     4,
       1,     1,     1,     2,     1,     4,     6,     5,     5,     4,
       2,     3,     1,     2,     3,     0,     2,     2,     2,     3,
       3,     3,     3,     3,     3,     3,     5,     4,     1,     1,
       1,     1,     1,     1,     1
};


#define yyerrok         (yyerrstatus = 0)
#define yyclearin       (yychar = YYEMPTY)
#define YYEMPTY         (-2)
#define YYEOF           0

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab


#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)                                    \
  do                                                              \
    if (yychar == YYEMPTY)                                        \
      {                                                           \
        yychar = (Token);                                         \
        yylval = (Value);                                         \
        YYPOPSTACK (yylen);                                       \
        yystate = *yyssp;                                         \
        goto yybackup;                                            \
      }                                                           \
    else                                                          \
      {                                                           \
        yyerror (&yylloc, scanner, YY_("syntax error: cannot back up")); \
        YYERROR;                                                  \
      }                                                           \
  while (0)

/* Error token number */
#define YYTERROR        1
#define YYERRCODE       256


/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

#ifndef YYLLOC_DEFAULT
# define YYLLOC_DEFAULT(Current, Rhs, N)                                \
    do                                                                  \
      if (N)                                                            \
        {                                                               \
          (Current).first_line   = YYRHSLOC (Rhs, 1).first_line;        \
          (Current).first_column = YYRHSLOC (Rhs, 1).first_column;      \
          (Current).last_line    = YYRHSLOC (Rhs, N).last_line;         \
          (Current).last_column  = YYRHSLOC (Rhs, N).last_column;       \
        }                                                               \
      else                                                              \
        {                                                               \
          (Current).first_line   = (Current).last_line   =              \
            YYRHSLOC (Rhs, 0).last_line;                                \
          (Current).first_column = (Current).last_column =              \
            YYRHSLOC (Rhs, 0).last_column;                              \
        }                                                               \
    while (0)
#endif

#define YYRHSLOC(Rhs, K) ((Rhs)[K])


/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)                        \
do {                                            \
  if (yydebug)                                  \
    YYFPRINTF Args;                             \
} while (0)


/* YY_LOCATION_PRINT -- Print the location on the stream.
   This macro was not mandated originally: define only if we know
   we won't break user code: when these are the locations we know.  */

#ifndef YY_LOCATION_PRINT
# if defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL

/* Print *YYLOCP on YYO.  Private, do not rely on its existence. */

YY_ATTRIBUTE_UNUSED
static int
yy_location_print_ (FILE *yyo, YYLTYPE const * const yylocp)
{
  int res = 0;
  int end_col = 0 != yylocp->last_column ? yylocp->last_column - 1 : 0;
  if (0 <= yylocp->first_line)
    {
      res += YYFPRINTF (yyo, "%d", yylocp->first_line);
      if (0 <= yylocp->first_column)
        res += YYFPRINTF (yyo, ".%d", yylocp->first_column);
    }
  if (0 <= yylocp->last_line)
    {
      if (yylocp->first_line < yylocp->last_line)
        {
          res += YYFPRINTF (yyo, "-%d", yylocp->last_line);
          if (0 <= end_col)
            res += YYFPRINTF (yyo, ".%d", end_col);
        }
      else if (0 <= end_col && yylocp->first_column < end_col)
        res += YYFPRINTF (yyo, "-%d", end_col);
    }
  return res;
 }

#  define YY_LOCATION_PRINT(File, Loc)          \
  yy_location_print_ (File, &(Loc))

# else
#  define YY_LOCATION_PRINT(File, Loc) ((void) 0)
# endif
#endif


# define YY_SYMBOL_PRINT(Title, Type, Value, Location)                    \
do {                                                                      \
  if (yydebug)                                                            \
    {                                                                     \
      YYFPRINTF (stderr, "%s ", Title);                                   \
      yy_symbol_print (stderr,                                            \
                  Type, Value, Location, scanner); \
      YYFPRINTF (stderr, "\n");                                           \
    }                                                                     \
} while (0)


/*-----------------------------------.
| Print this symbol's value on YYO.  |
`-----------------------------------*/

static void
yy_symbol_value_print (FILE *yyo, int yytype, YYSTYPE const * const yyvaluep, YYLTYPE const * const yylocationp, yyscan_t scanner)
{
  FILE *yyoutput = yyo;
  YYUSE (yyoutput);
  YYUSE (yylocationp);
  YYUSE (scanner);
  if (!yyvaluep)
    return;
# ifdef YYPRINT
  if (yytype < YYNTOKENS)
    YYPRINT (yyo, yytoknum[yytype], *yyvaluep);
# endif
  YYUSE (yytype);
}


/*---------------------------.
| Print this symbol on YYO.  |
`---------------------------*/

static void
yy_symbol_print (FILE *yyo, int yytype, YYSTYPE const * const yyvaluep, YYLTYPE const * const yylocationp, yyscan_t scanner)
{
  YYFPRINTF (yyo, "%s %s (",
             yytype < YYNTOKENS ? "token" : "nterm", yytname[yytype]);

  YY_LOCATION_PRINT (yyo, *yylocationp);
  YYFPRINTF (yyo, ": ");
  yy_symbol_value_print (yyo, yytype, yyvaluep, yylocationp, scanner);
  YYFPRINTF (yyo, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

static void
yy_stack_print (yytype_int16 *yybottom, yytype_int16 *yytop)
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)                            \
do {                                                            \
  if (yydebug)                                                  \
    yy_stack_print ((Bottom), (Top));                           \
} while (0)


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

static void
yy_reduce_print (yytype_int16 *yyssp, YYSTYPE *yyvsp, YYLTYPE *yylsp, int yyrule, yyscan_t scanner)
{
  unsigned long yylno = yyrline[yyrule];
  int yynrhs = yyr2[yyrule];
  int yyi;
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %lu):\n",
             yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr,
                       yystos[yyssp[yyi + 1 - yynrhs]],
                       &yyvsp[(yyi + 1) - (yynrhs)]
                       , &(yylsp[(yyi + 1) - (yynrhs)])                       , scanner);
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)          \
do {                                    \
  if (yydebug)                          \
    yy_reduce_print (yyssp, yyvsp, yylsp, Rule, scanner); \
} while (0)

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args)
# define YY_SYMBOL_PRINT(Title, Type, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif


#if YYERROR_VERBOSE

# ifndef yystrlen
#  if defined __GLIBC__ && defined _STRING_H
#   define yystrlen strlen
#  else
/* Return the length of YYSTR.  */
static YYSIZE_T
yystrlen (const char *yystr)
{
  YYSIZE_T yylen;
  for (yylen = 0; yystr[yylen]; yylen++)
    continue;
  return yylen;
}
#  endif
# endif

# ifndef yystpcpy
#  if defined __GLIBC__ && defined _STRING_H && defined _GNU_SOURCE
#   define yystpcpy stpcpy
#  else
/* Copy YYSRC to YYDEST, returning the address of the terminating '\0' in
   YYDEST.  */
static char *
yystpcpy (char *yydest, const char *yysrc)
{
  char *yyd = yydest;
  const char *yys = yysrc;

  while ((*yyd++ = *yys++) != '\0')
    continue;

  return yyd - 1;
}
#  endif
# endif

# ifndef yytnamerr
/* Copy to YYRES the contents of YYSTR after stripping away unnecessary
   quotes and backslashes, so that it's suitable for yyerror.  The
   heuristic is that double-quoting is unnecessary unless the string
   contains an apostrophe, a comma, or backslash (other than
   backslash-backslash).  YYSTR is taken from yytname.  If YYRES is
   null, do not copy; instead, return the length of what the result
   would have been.  */
static YYSIZE_T
yytnamerr (char *yyres, const char *yystr)
{
  if (*yystr == '"')
    {
      YYSIZE_T yyn = 0;
      char const *yyp = yystr;

      for (;;)
        switch (*++yyp)
          {
          case '\'':
          case ',':
            goto do_not_strip_quotes;

          case '\\':
            if (*++yyp != '\\')
              goto do_not_strip_quotes;
            else
              goto append;

          append:
          default:
            if (yyres)
              yyres[yyn] = *yyp;
            yyn++;
            break;

          case '"':
            if (yyres)
              yyres[yyn] = '\0';
            return yyn;
          }
    do_not_strip_quotes: ;
    }

  if (! yyres)
    return yystrlen (yystr);

  return (YYSIZE_T) (yystpcpy (yyres, yystr) - yyres);
}
# endif

/* Copy into *YYMSG, which is of size *YYMSG_ALLOC, an error message
   about the unexpected token YYTOKEN for the state stack whose top is
   YYSSP.

   Return 0 if *YYMSG was successfully written.  Return 1 if *YYMSG is
   not large enough to hold the message.  In that case, also set
   *YYMSG_ALLOC to the required number of bytes.  Return 2 if the
   required number of bytes is too large to store.  */
static int
yysyntax_error (YYSIZE_T *yymsg_alloc, char **yymsg,
                yytype_int16 *yyssp, int yytoken)
{
  YYSIZE_T yysize0 = yytnamerr (YY_NULLPTR, yytname[yytoken]);
  YYSIZE_T yysize = yysize0;
  enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
  /* Internationalized format string. */
  const char *yyformat = YY_NULLPTR;
  /* Arguments of yyformat. */
  char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];
  /* Number of reported tokens (one for the "unexpected", one per
     "expected"). */
  int yycount = 0;

  /* There are many possibilities here to consider:
     - If this state is a consistent state with a default action, then
       the only way this function was invoked is if the default action
       is an error action.  In that case, don't check for expected
       tokens because there are none.
     - The only way there can be no lookahead present (in yychar) is if
       this state is a consistent state with a default action.  Thus,
       detecting the absence of a lookahead is sufficient to determine
       that there is no unexpected or expected token to report.  In that
       case, just report a simple "syntax error".
     - Don't assume there isn't a lookahead just because this state is a
       consistent state with a default action.  There might have been a
       previous inconsistent state, consistent state with a non-default
       action, or user semantic action that manipulated yychar.
     - Of course, the expected token list depends on states to have
       correct lookahead information, and it depends on the parser not
       to perform extra reductions after fetching a lookahead from the
       scanner and before detecting a syntax error.  Thus, state merging
       (from LALR or IELR) and default reductions corrupt the expected
       token list.  However, the list is correct for canonical LR with
       one exception: it will still contain any token that will not be
       accepted due to an error action in a later state.
  */
  if (yytoken != YYEMPTY)
    {
      int yyn = yypact[*yyssp];
      yyarg[yycount++] = yytname[yytoken];
      if (!yypact_value_is_default (yyn))
        {
          /* Start YYX at -YYN if negative to avoid negative indexes in
             YYCHECK.  In other words, skip the first -YYN actions for
             this state because they are default actions.  */
          int yyxbegin = yyn < 0 ? -yyn : 0;
          /* Stay within bounds of both yycheck and yytname.  */
          int yychecklim = YYLAST - yyn + 1;
          int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
          int yyx;

          for (yyx = yyxbegin; yyx < yyxend; ++yyx)
            if (yycheck[yyx + yyn] == yyx && yyx != YYTERROR
                && !yytable_value_is_error (yytable[yyx + yyn]))
              {
                if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
                  {
                    yycount = 1;
                    yysize = yysize0;
                    break;
                  }
                yyarg[yycount++] = yytname[yyx];
                {
                  YYSIZE_T yysize1 = yysize + yytnamerr (YY_NULLPTR, yytname[yyx]);
                  if (yysize <= yysize1 && yysize1 <= YYSTACK_ALLOC_MAXIMUM)
                    yysize = yysize1;
                  else
                    return 2;
                }
              }
        }
    }

  switch (yycount)
    {
# define YYCASE_(N, S)                      \
      case N:                               \
        yyformat = S;                       \
      break
    default: /* Avoid compiler warnings. */
      YYCASE_(0, YY_("syntax error"));
      YYCASE_(1, YY_("syntax error, unexpected %s"));
      YYCASE_(2, YY_("syntax error, unexpected %s, expecting %s"));
      YYCASE_(3, YY_("syntax error, unexpected %s, expecting %s or %s"));
      YYCASE_(4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
      YYCASE_(5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
# undef YYCASE_
    }

  {
    YYSIZE_T yysize1 = yysize + yystrlen (yyformat);
    if (yysize <= yysize1 && yysize1 <= YYSTACK_ALLOC_MAXIMUM)
      yysize = yysize1;
    else
      return 2;
  }

  if (*yymsg_alloc < yysize)
    {
      *yymsg_alloc = 2 * yysize;
      if (! (yysize <= *yymsg_alloc
             && *yymsg_alloc <= YYSTACK_ALLOC_MAXIMUM))
        *yymsg_alloc = YYSTACK_ALLOC_MAXIMUM;
      return 1;
    }

  /* Avoid sprintf, as that infringes on the user's name space.
     Don't have undefined behavior even if the translation
     produced a string with the wrong number of "%s"s.  */
  {
    char *yyp = *yymsg;
    int yyi = 0;
    while ((*yyp = *yyformat) != '\0')
      if (*yyp == '%' && yyformat[1] == 's' && yyi < yycount)
        {
          yyp += yytnamerr (yyp, yyarg[yyi++]);
          yyformat += 2;
        }
      else
        {
          yyp++;
          yyformat++;
        }
  }
  return 0;
}
#endif /* YYERROR_VERBOSE */

/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

static void
yydestruct (const char *yymsg, int yytype, YYSTYPE *yyvaluep, YYLTYPE *yylocationp, yyscan_t scanner)
{
  YYUSE (yyvaluep);
  YYUSE (yylocationp);
  YYUSE (scanner);
  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yytype, yyvaluep, yylocationp);

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YYUSE (yytype);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}



struct yypstate
  {
    /* Number of syntax errors so far.  */
    int yynerrs;

    int yystate;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus;

    /* The stacks and their tools:
       'yyss': related to states.
       'yyvs': related to semantic values.
       'yyls': related to locations.

       Refer to the stacks through separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* The state stack.  */
    yytype_int16 yyssa[YYINITDEPTH];
    yytype_int16 *yyss;
    yytype_int16 *yyssp;

    /* The semantic value stack.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs;
    YYSTYPE *yyvsp;

    /* The location stack.  */
    YYLTYPE yylsa[YYINITDEPTH];
    YYLTYPE *yyls;
    YYLTYPE *yylsp;

    /* The locations where the error started and ended.  */
    YYLTYPE yyerror_range[3];

    YYSIZE_T yystacksize;
    /* Used to determine if this is the first time this instance has
       been used.  */
    int yynew;
  };

/* Initialize the parser data structure.  */
yypstate *
yypstate_new (void)
{
  yypstate *yyps;
  yyps = (yypstate *) malloc (sizeof *yyps);
  if (!yyps)
    return YY_NULLPTR;
  yyps->yynew = 1;
  return yyps;
}

void
yypstate_delete (yypstate *yyps)
{
  if (yyps)
    {
#ifndef yyoverflow
      /* If the stack was reallocated but the parse did not complete, then the
         stack still needs to be freed.  */
      if (!yyps->yynew && yyps->yyss != yyps->yyssa)
        YYSTACK_FREE (yyps->yyss);
#endif
      free (yyps);
    }
}

#define yynerrs yyps->yynerrs
#define yystate yyps->yystate
#define yyerrstatus yyps->yyerrstatus
#define yyssa yyps->yyssa
#define yyss yyps->yyss
#define yyssp yyps->yyssp
#define yyvsa yyps->yyvsa
#define yyvs yyps->yyvs
#define yyvsp yyps->yyvsp
#define yylsa yyps->yylsa
#define yyls yyps->yyls
#define yylsp yyps->yylsp
#define yyerror_range yyps->yyerror_range
#define yystacksize yyps->yystacksize


/*---------------.
| yypush_parse.  |
`---------------*/

int
yypush_parse (yypstate *yyps, int yypushed_char, YYSTYPE const *yypushed_val, YYLTYPE *yypushed_loc, yyscan_t scanner)
{
/* The lookahead symbol.  */
int yychar;


/* The semantic value of the lookahead symbol.  */
/* Default value used for initialization, for pacifying older GCCs
   or non-GCC compilers.  */
YY_INITIAL_VALUE (static YYSTYPE yyval_default;)
YYSTYPE yylval YY_INITIAL_VALUE (= yyval_default);

/* Location data for the lookahead symbol.  */
static YYLTYPE yyloc_default
# if defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL
  = { 1, 1, 1, 1 }
# endif
;
YYLTYPE yylloc = yyloc_default;

  int yyn;
  int yyresult;
  /* Lookahead token as an internal (translated) token number.  */
  int yytoken = 0;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;
  YYLTYPE yyloc;

#if YYERROR_VERBOSE
  /* Buffer for error messages, and its allocated size.  */
  char yymsgbuf[128];
  char *yymsg = yymsgbuf;
  YYSIZE_T yymsg_alloc = sizeof yymsgbuf;
#endif

#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N), yylsp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  if (!yyps->yynew)
    {
      yyn = yypact[yystate];
      goto yyread_pushed_token;
    }

  yyssp = yyss = yyssa;
  yyvsp = yyvs = yyvsa;
  yylsp = yyls = yylsa;
  yystacksize = YYINITDEPTH;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yystate = 0;
  yyerrstatus = 0;
  yynerrs = 0;
  yychar = YYEMPTY; /* Cause a token to be read.  */
  yylsp[0] = *yypushed_loc;
  goto yysetstate;


/*------------------------------------------------------------.
| yynewstate -- push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;


/*--------------------------------------------------------------------.
| yynewstate -- set current state (the top of the stack) to yystate.  |
`--------------------------------------------------------------------*/
yysetstate:
  YYDPRINTF ((stderr, "Entering state %d\n", yystate));
  YY_ASSERT (0 <= yystate && yystate < YYNSTATES);
  *yyssp = (yytype_int16) yystate;

  if (yyss + yystacksize - 1 <= yyssp)
#if !defined yyoverflow && !defined YYSTACK_RELOCATE
    goto yyexhaustedlab;
#else
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYSIZE_T yysize = (YYSIZE_T) (yyssp - yyss + 1);

# if defined yyoverflow
      {
        /* Give user a chance to reallocate the stack.  Use copies of
           these so that the &'s don't force the real ones into
           memory.  */
        YYSTYPE *yyvs1 = yyvs;
        yytype_int16 *yyss1 = yyss;
        YYLTYPE *yyls1 = yyls;

        /* Each stack pointer address is followed by the size of the
           data in use in that stack, in bytes.  This used to be a
           conditional around just the two extra args, but that might
           be undefined if yyoverflow is a macro.  */
        yyoverflow (YY_("memory exhausted"),
                    &yyss1, yysize * sizeof (*yyssp),
                    &yyvs1, yysize * sizeof (*yyvsp),
                    &yyls1, yysize * sizeof (*yylsp),
                    &yystacksize);
        yyss = yyss1;
        yyvs = yyvs1;
        yyls = yyls1;
      }
# else /* defined YYSTACK_RELOCATE */
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
        goto yyexhaustedlab;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
        yystacksize = YYMAXDEPTH;

      {
        yytype_int16 *yyss1 = yyss;
        union yyalloc *yyptr =
          (union yyalloc *) YYSTACK_ALLOC (YYSTACK_BYTES (yystacksize));
        if (! yyptr)
          goto yyexhaustedlab;
        YYSTACK_RELOCATE (yyss_alloc, yyss);
        YYSTACK_RELOCATE (yyvs_alloc, yyvs);
        YYSTACK_RELOCATE (yyls_alloc, yyls);
# undef YYSTACK_RELOCATE
        if (yyss1 != yyssa)
          YYSTACK_FREE (yyss1);
      }
# endif

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;
      yylsp = yyls + yysize - 1;

      YYDPRINTF ((stderr, "Stack size increased to %lu\n",
                  (unsigned long) yystacksize));

      if (yyss + yystacksize - 1 <= yyssp)
        YYABORT;
    }
#endif /* !defined yyoverflow && !defined YYSTACK_RELOCATE */

  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;


/*-----------.
| yybackup.  |
`-----------*/
yybackup:
  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yypact_value_is_default (yyn))
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either YYEMPTY or YYEOF or a valid lookahead symbol.  */
  if (yychar == YYEMPTY)
    {
      if (!yyps->yynew)
        {
          YYDPRINTF ((stderr, "Return for a new token:\n"));
          yyresult = YYPUSH_MORE;
          goto yypushreturn;
        }
      yyps->yynew = 0;
yyread_pushed_token:
      YYDPRINTF ((stderr, "Reading a token: "));
      yychar = yypushed_char;
      if (yypushed_val)
        yylval = *yypushed_val;
      if (yypushed_loc)
        yylloc = *yypushed_loc;
    }

  if (yychar <= YYEOF)
    {
      yychar = yytoken = YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yytable_value_is_error (yyn))
        goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);

  /* Discard the shifted token.  */
  yychar = YYEMPTY;

  yystate = yyn;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END
  *++yylsp = yylloc;
  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     '$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];

  /* Default location. */
  YYLLOC_DEFAULT (yyloc, (yylsp - yylen), yylen);
  yyerror_range[1] = yyloc;
  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
  case 2:
#line 44 "src/luke/parser/compiled/tmp.y"
    { yyval = PyUnicode_FromString(strdup(yyvsp[0])); }
#line 2307 "tmp.tab.c"
    break;

  case 3:
#line 45 "src/luke/parser/compiled/tmp.y"
    { yyval = yyvsp[0]; }
#line 2313 "tmp.tab.c"
    break;

  case 4:
#line 46 "src/luke/parser/compiled/tmp.y"
    {
                        char * new_str ;
                        if((new_str = malloc(strlen(yyvsp[-1])+strlen(yyvsp[0])+1)) != NULL) {
                            new_str[0] = '\0';   // ensures the memory is an empty string
                            strcpy(new_str,yyvsp[-1]);
                            strcat(new_str,yyvsp[0]);
                        }
                        yyval = new_str;
                    }
#line 2327 "tmp.tab.c"
    break;

  case 5:
#line 62 "src/luke/parser/compiled/tmp.y"
    { yyval = PyUnicode_FromString(strdup(yyvsp[0])); }
#line 2333 "tmp.tab.c"
    break;

  case 6:
#line 63 "src/luke/parser/compiled/tmp.y"
    { yyval = yyvsp[0]; }
#line 2339 "tmp.tab.c"
    break;

  case 7:
#line 64 "src/luke/parser/compiled/tmp.y"
    {
                        char * new_str ;
                        if((new_str = malloc(strlen(yyvsp[-1])+strlen(yyvsp[0])+1)) != NULL) {
                            new_str[0] = '\0';   // ensures the memory is an empty string
                            strcpy(new_str,yyvsp[-1]);
                            strcat(new_str,yyvsp[0]);
                        }
                        yyval = new_str;
                    }
#line 2353 "tmp.tab.c"
    break;

  case 8:
#line 80 "src/luke/parser/compiled/tmp.y"
    { yyval = PyUnicode_FromString(strdup(yyvsp[0])); }
#line 2359 "tmp.tab.c"
    break;

  case 9:
#line 81 "src/luke/parser/compiled/tmp.y"
    { yyval = yyvsp[0]; }
#line 2365 "tmp.tab.c"
    break;

  case 10:
#line 82 "src/luke/parser/compiled/tmp.y"
    {
                        char * new_str ;
                        if((new_str = malloc(strlen(yyvsp[-1])+strlen(yyvsp[0])+1)) != NULL) {
                            new_str[0] = '\0';   // ensures the memory is an empty string
                            strcpy(new_str,yyvsp[-1]);
                            strcat(new_str,yyvsp[0]);
                        }
                        yyval = new_str;
                    }
#line 2379 "tmp.tab.c"
    break;

  case 11:
#line 92 "src/luke/parser/compiled/tmp.y"
    {{
                    char * new_str ;
                    if((new_str = malloc(1)) != NULL) {{
                        new_str[0] = '\0';
                    }}
                    yyval = new_str;
                  }}
#line 2391 "tmp.tab.c"
    break;

  case 12:
#line 106 "src/luke/parser/compiled/tmp.y"
    { yyval = PyUnicode_FromString(strdup(yyvsp[0])); }
#line 2397 "tmp.tab.c"
    break;

  case 13:
#line 107 "src/luke/parser/compiled/tmp.y"
    { yyval = yyvsp[0]; }
#line 2403 "tmp.tab.c"
    break;

  case 14:
#line 108 "src/luke/parser/compiled/tmp.y"
    {
                        char * new_str ;
                        if((new_str = malloc(strlen(yyvsp[-1])+strlen(yyvsp[0])+1)) != NULL) {
                            new_str[0] = '\0';   // ensures the memory is an empty string
                            strcpy(new_str,yyvsp[-1]);
                            strcat(new_str,yyvsp[0]);
                        }
                        yyval = new_str;
                    }
#line 2417 "tmp.tab.c"
    break;

  case 15:
#line 118 "src/luke/parser/compiled/tmp.y"
    {{
                    char * new_str ;
                    if((new_str = malloc(1)) != NULL) {{
                        new_str[0] = '\0';
                    }}
                    yyval = new_str;
                  }}
#line 2429 "tmp.tab.c"
    break;

  case 16:
#line 132 "src/luke/parser/compiled/tmp.y"
    { yyval = PyUnicode_FromString(strdup(yyvsp[0])); }
#line 2435 "tmp.tab.c"
    break;

  case 17:
#line 133 "src/luke/parser/compiled/tmp.y"
    { yyval = yyvsp[0]; }
#line 2441 "tmp.tab.c"
    break;

  case 18:
#line 134 "src/luke/parser/compiled/tmp.y"
    {
                        char * new_str ;
                        if((new_str = malloc(strlen(yyvsp[-1])+strlen(yyvsp[0])+1)) != NULL) {
                            new_str[0] = '\0';   // ensures the memory is an empty string
                            strcpy(new_str,yyvsp[-1]);
                            strcat(new_str,yyvsp[0]);
                        }
                        yyval = new_str;
                    }
#line 2455 "tmp.tab.c"
    break;

  case 19:
#line 144 "src/luke/parser/compiled/tmp.y"
    {{
                    char * new_str ;
                    if((new_str = malloc(1)) != NULL) {{
                        new_str[0] = '\0';
                    }}
                    yyval = new_str;
                  }}
#line 2467 "tmp.tab.c"
    break;

  case 20:
#line 158 "src/luke/parser/compiled/tmp.y"
    { yyval = PyUnicode_FromString(strdup(yyvsp[0])); }
#line 2473 "tmp.tab.c"
    break;

  case 21:
#line 159 "src/luke/parser/compiled/tmp.y"
    { yyval = yyvsp[0]; }
#line 2479 "tmp.tab.c"
    break;

  case 22:
#line 160 "src/luke/parser/compiled/tmp.y"
    {
                        char * new_str ;
                        if((new_str = malloc(strlen(yyvsp[-1])+strlen(yyvsp[0])+1)) != NULL) {
                            new_str[0] = '\0';   // ensures the memory is an empty string
                            strcpy(new_str,yyvsp[-1]);
                            strcat(new_str,yyvsp[0]);
                        }
                        yyval = new_str;
                    }
#line 2493 "tmp.tab.c"
    break;

  case 23:
#line 170 "src/luke/parser/compiled/tmp.y"
    {{
                    char * new_str ;
                    if((new_str = malloc(1)) != NULL) {{
                        new_str[0] = '\0';
                    }}
                    yyval = new_str;
                  }}
#line 2505 "tmp.tab.c"
    break;

  case 24:
#line 184 "src/luke/parser/compiled/tmp.y"
    { yyval = PyUnicode_FromString(strdup(yyvsp[0])); }
#line 2511 "tmp.tab.c"
    break;

  case 25:
#line 185 "src/luke/parser/compiled/tmp.y"
    { yyval = yyvsp[0]; }
#line 2517 "tmp.tab.c"
    break;

  case 26:
#line 186 "src/luke/parser/compiled/tmp.y"
    {
                        char * new_str ;
                        if((new_str = malloc(strlen(yyvsp[-1])+strlen(yyvsp[0])+1)) != NULL) {
                            new_str[0] = '\0';   // ensures the memory is an empty string
                            strcpy(new_str,yyvsp[-1]);
                            strcat(new_str,yyvsp[0]);
                        }
                        yyval = new_str;
                    }
#line 2531 "tmp.tab.c"
    break;

  case 27:
#line 196 "src/luke/parser/compiled/tmp.y"
    {{
                    char * new_str ;
                    if((new_str = malloc(1)) != NULL) {{
                        new_str[0] = '\0';
                    }}
                    yyval = new_str;
                  }}
#line 2543 "tmp.tab.c"
    break;

  case 28:
#line 208 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "input_start", 0, 1,
            "input", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2561 "tmp.tab.c"
    break;

  case 29:
#line 225 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "input", 0, 1,
            "blocks", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2579 "tmp.tab.c"
    break;

  case 30:
#line 239 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "input", 1, 2,
            "blocks", yyvsp[-1],
            "br_end", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2598 "tmp.tab.c"
    break;

  case 31:
#line 254 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "input", 2, 3,
            "br", yyvsp[-2],
            "blocks", yyvsp[-1],
            "br_end", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2618 "tmp.tab.c"
    break;

  case 32:
#line 270 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "input", 3, 2,
            "br", yyvsp[-1],
            "blocks", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2637 "tmp.tab.c"
    break;

  case 33:
#line 285 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "input", 4, 1,
            "br_end", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2655 "tmp.tab.c"
    break;

  case 34:
#line 299 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "input", 5, 0,
            NULL
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2673 "tmp.tab.c"
    break;

  case 35:
#line 316 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "blocks", 0, 1,
            "block", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2691 "tmp.tab.c"
    break;

  case 36:
#line 330 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "blocks", 1, 3,
            "blocks", yyvsp[-2],
            "br", yyvsp[-1],
            "block", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2711 "tmp.tab.c"
    break;

  case 37:
#line 349 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "block", 0, 1,
            "header", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2729 "tmp.tab.c"
    break;

  case 38:
#line 363 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "block", 1, 1,
            "text", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2747 "tmp.tab.c"
    break;

  case 39:
#line 377 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "block", 2, 1,
            "ulist", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2765 "tmp.tab.c"
    break;

  case 40:
#line 391 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "block", 3, 1,
            "olist", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2783 "tmp.tab.c"
    break;

  case 41:
#line 405 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "block", 4, 1,
            "quote", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2801 "tmp.tab.c"
    break;

  case 42:
#line 419 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "block", 5, 1,
            "indent", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2819 "tmp.tab.c"
    break;

  case 43:
#line 433 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "block", 6, 1,
            "HRULE", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2837 "tmp.tab.c"
    break;

  case 44:
#line 447 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "block", 7, 1,
            "attributes", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2855 "tmp.tab.c"
    break;

  case 45:
#line 461 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "block", 8, 1,
            "table", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2873 "tmp.tab.c"
    break;

  case 46:
#line 475 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "block", 9, 1,
            "codeblock_block", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2891 "tmp.tab.c"
    break;

  case 47:
#line 489 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "block", 10, 1,
            "href_definition", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2909 "tmp.tab.c"
    break;

  case 48:
#line 503 "src/luke/parser/compiled/tmp.y"
    {
             yyerrok;
             PyObject* lasterr = PyObject_GetAttrString((PyObject*)py_parser, "lasterror");;
          yyval = (*py_callback)(
            py_parser, "block", 11, 1,
            "error", lasterr
            );
 PyObject_SetAttrString(py_parser, "lasterror", Py_None);
             Py_DECREF(lasterr);
             Py_INCREF(Py_None);
             yyclearin;
        }
#line 2926 "tmp.tab.c"
    break;

  case 49:
#line 519 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "br", 0, 1,
            "BR", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2944 "tmp.tab.c"
    break;

  case 50:
#line 533 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "br", 1, 1,
            "NEWLINE", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2962 "tmp.tab.c"
    break;

  case 51:
#line 547 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "br", 2, 2,
            "br", yyvsp[-1],
            "BR", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 2981 "tmp.tab.c"
    break;

  case 52:
#line 562 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "br", 3, 3,
            "br", yyvsp[-2],
            "INDENT_SYM", yyvsp[-1],
            "BR", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3001 "tmp.tab.c"
    break;

  case 53:
#line 581 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "br_end", 0, 1,
            "br", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3019 "tmp.tab.c"
    break;

  case 54:
#line 595 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "br_end", 1, 2,
            "br", yyvsp[-1],
            "INDENT_SYM", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3038 "tmp.tab.c"
    break;

  case 55:
#line 613 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "indent", 0, 2,
            "INDENT_SYM", yyvsp[-1],
            "text", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3057 "tmp.tab.c"
    break;

  case 56:
#line 631 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "quote", 0, 3,
            "QUOTE_SYM", yyvsp[-2],
            "text", yyvsp[-1],
            "attributes", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3077 "tmp.tab.c"
    break;

  case 57:
#line 647 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "quote", 1, 2,
            "QUOTE_SYM", yyvsp[-1],
            "attributes", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3096 "tmp.tab.c"
    break;

  case 58:
#line 662 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "quote", 2, 2,
            "QUOTE_SYM", yyvsp[-1],
            "text", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3115 "tmp.tab.c"
    break;

  case 59:
#line 677 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "quote", 3, 1,
            "QUOTE_SYM", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3133 "tmp.tab.c"
    break;

  case 60:
#line 694 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "ulist", 0, 3,
            "ULIST_SYM", yyvsp[-2],
            "text", yyvsp[-1],
            "attributes", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3153 "tmp.tab.c"
    break;

  case 61:
#line 710 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "ulist", 1, 2,
            "ULIST_SYM", yyvsp[-1],
            "attributes", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3172 "tmp.tab.c"
    break;

  case 62:
#line 725 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "ulist", 2, 2,
            "ULIST_SYM", yyvsp[-1],
            "text", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3191 "tmp.tab.c"
    break;

  case 63:
#line 740 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "ulist", 3, 1,
            "ULIST_SYM", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3209 "tmp.tab.c"
    break;

  case 64:
#line 757 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "olist", 0, 3,
            "OLIST_SYM", yyvsp[-2],
            "text", yyvsp[-1],
            "attributes", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3229 "tmp.tab.c"
    break;

  case 65:
#line 773 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "olist", 1, 2,
            "OLIST_SYM", yyvsp[-1],
            "attributes", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3248 "tmp.tab.c"
    break;

  case 66:
#line 788 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "olist", 2, 2,
            "OLIST_SYM", yyvsp[-1],
            "text", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3267 "tmp.tab.c"
    break;

  case 67:
#line 803 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "olist", 3, 1,
            "OLIST_SYM", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3285 "tmp.tab.c"
    break;

  case 68:
#line 820 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "href_definition", 0, 2,
            "IMAGE_DEFINITION", yyvsp[-1],
            "URL", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3304 "tmp.tab.c"
    break;

  case 69:
#line 835 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "href_definition", 1, 2,
            "LINK_DEFINITION", yyvsp[-1],
            "URL", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3323 "tmp.tab.c"
    break;

  case 70:
#line 850 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "href_definition", 2, 3,
            "IMAGE_DEFINITION", yyvsp[-2],
            "URL", yyvsp[-1],
            "text", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3343 "tmp.tab.c"
    break;

  case 71:
#line 866 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "href_definition", 3, 3,
            "LINK_DEFINITION", yyvsp[-2],
            "URL", yyvsp[-1],
            "text", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3363 "tmp.tab.c"
    break;

  case 72:
#line 882 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "href_definition", 4, 2,
            "FOOTNOTE_DEFINITION", yyvsp[-1],
            "text", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3382 "tmp.tab.c"
    break;

  case 73:
#line 897 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "href_definition", 5, 1,
            "FOOTNOTE_DEFINITION", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3400 "tmp.tab.c"
    break;

  case 74:
#line 914 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "header", 0, 1,
            "header_hash", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3418 "tmp.tab.c"
    break;

  case 75:
#line 928 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "header", 1, 3,
            "text", yyvsp[-2],
            "attributes", yyvsp[-1],
            "HEADING_ULINEDBL", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3438 "tmp.tab.c"
    break;

  case 76:
#line 944 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "header", 2, 3,
            "text", yyvsp[-2],
            "attributes", yyvsp[-1],
            "HEADING_ULINESGL", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3458 "tmp.tab.c"
    break;

  case 77:
#line 960 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "header", 3, 2,
            "text", yyvsp[-1],
            "HEADING_ULINEDBL", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3477 "tmp.tab.c"
    break;

  case 78:
#line 975 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "header", 4, 2,
            "text", yyvsp[-1],
            "HEADING_ULINESGL", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3496 "tmp.tab.c"
    break;

  case 79:
#line 993 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "header_hash", 0, 3,
            "HEADINGHASH_END", yyvsp[-2],
            "text", yyvsp[-1],
            "attributes", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3516 "tmp.tab.c"
    break;

  case 80:
#line 1009 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "header_hash", 1, 2,
            "HEADINGHASH_END", yyvsp[-1],
            "text", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3535 "tmp.tab.c"
    break;

  case 81:
#line 1024 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "header_hash", 2, 2,
            "HEADINGHASH", yyvsp[-1],
            "header_hash", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3554 "tmp.tab.c"
    break;

  case 82:
#line 1042 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "text", 0, 1,
            "span", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3572 "tmp.tab.c"
    break;

  case 83:
#line 1056 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "text", 1, 2,
            "attributes", yyvsp[-1],
            "span", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3591 "tmp.tab.c"
    break;

  case 84:
#line 1071 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "text", 2, 2,
            "text", yyvsp[-1],
            "span", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3610 "tmp.tab.c"
    break;

  case 85:
#line 1086 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "text", 3, 3,
            "text", yyvsp[-2],
            "attributes", yyvsp[-1],
            "span", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3630 "tmp.tab.c"
    break;

  case 86:
#line 1105 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span", 0, 1,
            "string", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3648 "tmp.tab.c"
    break;

  case 87:
#line 1119 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span", 1, 3,
            "EMPH_START", yyvsp[-2],
            "span_multitext_wrap", yyvsp[-1],
            "EMPH_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3668 "tmp.tab.c"
    break;

  case 88:
#line 1135 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span", 2, 3,
            "STRONG_START", yyvsp[-2],
            "span_multitext_wrap", yyvsp[-1],
            "STRONG_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3688 "tmp.tab.c"
    break;

  case 89:
#line 1151 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span", 3, 3,
            "ITALIC_START", yyvsp[-2],
            "span_multitext_wrap", yyvsp[-1],
            "ITALIC_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3708 "tmp.tab.c"
    break;

  case 90:
#line 1167 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span", 4, 3,
            "BOLD_START", yyvsp[-2],
            "span_multitext_wrap", yyvsp[-1],
            "BOLD_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3728 "tmp.tab.c"
    break;

  case 91:
#line 1183 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span", 5, 3,
            "STRIKE_START", yyvsp[-2],
            "span_multitext_wrap", yyvsp[-1],
            "STRIKE_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3748 "tmp.tab.c"
    break;

  case 92:
#line 1199 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span", 6, 1,
            "math", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3766 "tmp.tab.c"
    break;

  case 93:
#line 1213 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span", 7, 3,
            "CODEINLINE_START", yyvsp[-2],
            "codeinline_string", yyvsp[-1],
            "CODEINLINE_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3786 "tmp.tab.c"
    break;

  case 94:
#line 1229 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span", 8, 1,
            "hyperref", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3804 "tmp.tab.c"
    break;

  case 95:
#line 1243 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span", 9, 1,
            "latex", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3822 "tmp.tab.c"
    break;

  case 96:
#line 1257 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span", 10, 1,
            "PLACEHOLDER", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3840 "tmp.tab.c"
    break;

  case 97:
#line 1271 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span", 11, 2,
            "EMPH_START", yyvsp[-1],
            "span_multitext_wrap", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3859 "tmp.tab.c"
    break;

  case 98:
#line 1286 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span", 12, 2,
            "STRONG_START", yyvsp[-1],
            "span_multitext_wrap", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3878 "tmp.tab.c"
    break;

  case 99:
#line 1301 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span", 13, 2,
            "ITALIC_START", yyvsp[-1],
            "span_multitext_wrap", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3897 "tmp.tab.c"
    break;

  case 100:
#line 1316 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span", 14, 2,
            "BOLD_START", yyvsp[-1],
            "span_multitext_wrap", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3916 "tmp.tab.c"
    break;

  case 101:
#line 1331 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span", 15, 2,
            "STRIKE_START", yyvsp[-1],
            "span_multitext_wrap", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3935 "tmp.tab.c"
    break;

  case 102:
#line 1346 "src/luke/parser/compiled/tmp.y"
    {
             yyerrok;
             PyObject* lasterr = PyObject_GetAttrString((PyObject*)py_parser, "lasterror");;
          yyval = (*py_callback)(
            py_parser, "span", 16, 2,
            "error", lasterr,
            "UNEXPECTED_END", yyvsp[0]
            );
 PyObject_SetAttrString(py_parser, "lasterror", Py_None);
             Py_DECREF(lasterr);
             Py_INCREF(Py_None);
             yyclearin;
        }
#line 3953 "tmp.tab.c"
    break;

  case 103:
#line 1363 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span_multitext_wrap", 0, 1,
            "span_multitext", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3971 "tmp.tab.c"
    break;

  case 104:
#line 1377 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span_multitext_wrap", 1, 2,
            "br", yyvsp[-1],
            "span_multitext", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 3990 "tmp.tab.c"
    break;

  case 105:
#line 1395 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span_multitext", 0, 1,
            "text", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4008 "tmp.tab.c"
    break;

  case 106:
#line 1409 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span_multitext", 1, 3,
            "text", yyvsp[-2],
            "br", yyvsp[-1],
            "span_multitext", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4028 "tmp.tab.c"
    break;

  case 107:
#line 1425 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "span_multitext", 2, 0,
            NULL
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4046 "tmp.tab.c"
    break;

  case 108:
#line 1442 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "latex", 0, 1,
            "LATEX_COMMAND", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4064 "tmp.tab.c"
    break;

  case 109:
#line 1456 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "latex", 1, 3,
            "latex_command_with_arguments", yyvsp[-2],
            "input", yyvsp[-1],
            "HYPERREF_REF_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4084 "tmp.tab.c"
    break;

  case 110:
#line 1472 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "latex", 2, 3,
            "LATEX_COMMAND_WITH_OPTIONAL_ARGUMENT", yyvsp[-2],
            "attribute_list", yyvsp[-1],
            "ATTR_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4104 "tmp.tab.c"
    break;

  case 111:
#line 1488 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "latex", 3, 3,
            "latex_command_with_arguments_and_optional", yyvsp[-2],
            "input", yyvsp[-1],
            "HYPERREF_REF_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4124 "tmp.tab.c"
    break;

  case 112:
#line 1504 "src/luke/parser/compiled/tmp.y"
    {
             yyerrok;
             PyObject* lasterr = PyObject_GetAttrString((PyObject*)py_parser, "lasterror");;
          yyval = (*py_callback)(
            py_parser, "latex", 4, 2,
            "latex_command_with_arguments", yyvsp[-1],
            "error", lasterr
            );
 PyObject_SetAttrString(py_parser, "lasterror", Py_None);
             Py_DECREF(lasterr);
             Py_INCREF(Py_None);
             yyclearin;
        }
#line 4142 "tmp.tab.c"
    break;

  case 113:
#line 1518 "src/luke/parser/compiled/tmp.y"
    {
             yyerrok;
             PyObject* lasterr = PyObject_GetAttrString((PyObject*)py_parser, "lasterror");;
          yyval = (*py_callback)(
            py_parser, "latex", 5, 2,
            "latex_command_with_arguments_and_optional", yyvsp[-1],
            "error", lasterr
            );
 PyObject_SetAttrString(py_parser, "lasterror", Py_None);
             Py_DECREF(lasterr);
             Py_INCREF(Py_None);
             yyclearin;
        }
#line 4160 "tmp.tab.c"
    break;

  case 114:
#line 1535 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "latex_command_with_arguments_and_optional", 0, 3,
            "LATEX_COMMAND_WITH_OPTIONAL_ARGUMENT", yyvsp[-2],
            "attribute_list", yyvsp[-1],
            "ATTR_END_AND_ARG_START", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4180 "tmp.tab.c"
    break;

  case 115:
#line 1551 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "latex_command_with_arguments_and_optional", 1, 3,
            "latex_command_with_arguments_and_optional", yyvsp[-2],
            "input", yyvsp[-1],
            "HYPERREF_REF_MID", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4200 "tmp.tab.c"
    break;

  case 116:
#line 1567 "src/luke/parser/compiled/tmp.y"
    {
             yyerrok;
             PyObject* lasterr = PyObject_GetAttrString((PyObject*)py_parser, "lasterror");;
          yyval = (*py_callback)(
            py_parser, "latex_command_with_arguments_and_optional", 2, 2,
            "latex_command_with_arguments_and_optional", yyvsp[-1],
            "error", lasterr
            );
 PyObject_SetAttrString(py_parser, "lasterror", Py_None);
             Py_DECREF(lasterr);
             Py_INCREF(Py_None);
             yyclearin;
        }
#line 4218 "tmp.tab.c"
    break;

  case 117:
#line 1584 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "latex_command_with_arguments", 0, 1,
            "LATEX_COMMAND_WITH_ARGUMENTS", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4236 "tmp.tab.c"
    break;

  case 118:
#line 1598 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "latex_command_with_arguments", 1, 3,
            "latex_command_with_arguments", yyvsp[-2],
            "input", yyvsp[-1],
            "HYPERREF_REF_MID", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4256 "tmp.tab.c"
    break;

  case 119:
#line 1614 "src/luke/parser/compiled/tmp.y"
    {
             yyerrok;
             PyObject* lasterr = PyObject_GetAttrString((PyObject*)py_parser, "lasterror");;
          yyval = (*py_callback)(
            py_parser, "latex_command_with_arguments", 2, 2,
            "latex_command_with_arguments", yyvsp[-1],
            "error", lasterr
            );
 PyObject_SetAttrString(py_parser, "lasterror", Py_None);
             Py_DECREF(lasterr);
             Py_INCREF(Py_None);
             yyclearin;
        }
#line 4274 "tmp.tab.c"
    break;

  case 120:
#line 1631 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table", 0, 1,
            "table_delim", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4292 "tmp.tab.c"
    break;

  case 121:
#line 1645 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table", 1, 1,
            "table_no_delim", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4310 "tmp.tab.c"
    break;

  case 122:
#line 1659 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table", 2, 1,
            "table_delim_separator", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4328 "tmp.tab.c"
    break;

  case 123:
#line 1673 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table", 3, 1,
            "table_no_delim_separator", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4346 "tmp.tab.c"
    break;

  case 124:
#line 1687 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table", 4, 2,
            "INDENT_SYM", yyvsp[-1],
            "table", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4365 "tmp.tab.c"
    break;

  case 125:
#line 1705 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table_delim", 0, 3,
            "TABLE_DELIM", yyvsp[-2],
            "text", yyvsp[-1],
            "TABLE_DELIM", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4385 "tmp.tab.c"
    break;

  case 126:
#line 1721 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table_delim", 1, 3,
            "table_delim", yyvsp[-2],
            "text", yyvsp[-1],
            "TABLE_DELIM", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4405 "tmp.tab.c"
    break;

  case 127:
#line 1737 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table_delim", 2, 2,
            "TABLE_DELIM", yyvsp[-1],
            "TABLE_DELIM", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4424 "tmp.tab.c"
    break;

  case 128:
#line 1752 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table_delim", 3, 2,
            "table_delim", yyvsp[-1],
            "TABLE_DELIM", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4443 "tmp.tab.c"
    break;

  case 129:
#line 1770 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table_no_delim", 0, 3,
            "text", yyvsp[-2],
            "TABLE_DELIM", yyvsp[-1],
            "text", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4463 "tmp.tab.c"
    break;

  case 130:
#line 1786 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table_no_delim", 1, 3,
            "table_no_delim", yyvsp[-2],
            "TABLE_DELIM", yyvsp[-1],
            "text", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4483 "tmp.tab.c"
    break;

  case 131:
#line 1805 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table_delim_separator", 0, 3,
            "TABLE_DELIM", yyvsp[-2],
            "table_alignment", yyvsp[-1],
            "TABLE_DELIM", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4503 "tmp.tab.c"
    break;

  case 132:
#line 1821 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table_delim_separator", 1, 3,
            "table_delim_separator", yyvsp[-2],
            "table_alignment", yyvsp[-1],
            "TABLE_DELIM", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4523 "tmp.tab.c"
    break;

  case 133:
#line 1840 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table_no_delim_separator", 0, 3,
            "table_alignment", yyvsp[-2],
            "TABLE_DELIM", yyvsp[-1],
            "table_alignment", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4543 "tmp.tab.c"
    break;

  case 134:
#line 1856 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table_no_delim_separator", 1, 3,
            "table_no_delim_separator", yyvsp[-2],
            "TABLE_DELIM", yyvsp[-1],
            "table_alignment", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4563 "tmp.tab.c"
    break;

  case 135:
#line 1875 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table_alignment", 0, 1,
            "TABLE_HRULE", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4581 "tmp.tab.c"
    break;

  case 136:
#line 1889 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table_alignment", 1, 1,
            "TABLE_HRULE_CENTERED", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4599 "tmp.tab.c"
    break;

  case 137:
#line 1903 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table_alignment", 2, 1,
            "TABLE_HRULE_LEFT_ALIGNED", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4617 "tmp.tab.c"
    break;

  case 138:
#line 1917 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table_alignment", 3, 1,
            "TABLE_HRULE_RIGHT_ALIGNED", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4635 "tmp.tab.c"
    break;

  case 139:
#line 1931 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "table_alignment", 4, 2,
            "attributes", yyvsp[-1],
            "table_alignment", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4654 "tmp.tab.c"
    break;

  case 140:
#line 1949 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "hyperref", 0, 5,
            "hyperref_start", yyvsp[-4],
            "input", yyvsp[-3],
            "HYPERREF_LINK_MID", yyvsp[-2],
            "hyperref_link_string", yyvsp[-1],
            "HYPERREF_LINK_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4676 "tmp.tab.c"
    break;

  case 141:
#line 1967 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "hyperref", 1, 7,
            "hyperref_start", yyvsp[-6],
            "input", yyvsp[-5],
            "HYPERREF_LINK_MID", yyvsp[-4],
            "hyperref_link_string", yyvsp[-3],
            "HYPERREF_LINK_ALT_START", yyvsp[-2],
            "hyperref_link_alt_string", yyvsp[-1],
            "HYPERREF_LINK_ALT_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4700 "tmp.tab.c"
    break;

  case 142:
#line 1987 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "hyperref", 2, 5,
            "hyperref_start", yyvsp[-4],
            "input", yyvsp[-3],
            "HYPERREF_REF_MID", yyvsp[-2],
            "string", yyvsp[-1],
            "HYPERREF_REF_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4722 "tmp.tab.c"
    break;

  case 143:
#line 2005 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "hyperref", 3, 3,
            "hyperref_start", yyvsp[-2],
            "string", yyvsp[-1],
            "HYPERREF_REF_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4742 "tmp.tab.c"
    break;

  case 144:
#line 2021 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "hyperref", 4, 1,
            "URL", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4760 "tmp.tab.c"
    break;

  case 145:
#line 2035 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "hyperref", 5, 3,
            "FOOTNOTE_START", yyvsp[-2],
            "string", yyvsp[-1],
            "HYPERREF_REF_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4780 "tmp.tab.c"
    break;

  case 146:
#line 2051 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "hyperref", 6, 3,
            "FOOTNOTE_INLINE_START", yyvsp[-2],
            "input", yyvsp[-1],
            "HYPERREF_REF_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4800 "tmp.tab.c"
    break;

  case 147:
#line 2067 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "hyperref", 7, 5,
            "hyperref_start", yyvsp[-4],
            "input", yyvsp[-3],
            "FOOTNOTE_MID", yyvsp[-2],
            "string", yyvsp[-1],
            "HYPERREF_REF_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4822 "tmp.tab.c"
    break;

  case 148:
#line 2085 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "hyperref", 8, 5,
            "hyperref_start", yyvsp[-4],
            "input", yyvsp[-3],
            "FOOTNOTE_INLINE_MID", yyvsp[-2],
            "input", yyvsp[-1],
            "HYPERREF_REF_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4844 "tmp.tab.c"
    break;

  case 149:
#line 2103 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "hyperref", 9, 5,
            "hyperref_start", yyvsp[-4],
            "input", yyvsp[-3],
            "HYPERREF_CODE_START", yyvsp[-2],
            "hyperref_code_string", yyvsp[-1],
            "HYPERREF_CODE_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4866 "tmp.tab.c"
    break;

  case 150:
#line 2121 "src/luke/parser/compiled/tmp.y"
    {
             yyerrok;
             PyObject* lasterr = PyObject_GetAttrString((PyObject*)py_parser, "lasterror");;
          yyval = (*py_callback)(
            py_parser, "hyperref", 10, 2,
            "hyperref_start", yyvsp[-1],
            "error", lasterr
            );
 PyObject_SetAttrString(py_parser, "lasterror", Py_None);
             Py_DECREF(lasterr);
             Py_INCREF(Py_None);
             yyclearin;
        }
#line 4884 "tmp.tab.c"
    break;

  case 151:
#line 2135 "src/luke/parser/compiled/tmp.y"
    {
             yyerrok;
             PyObject* lasterr = PyObject_GetAttrString((PyObject*)py_parser, "lasterror");;
          yyval = (*py_callback)(
            py_parser, "hyperref", 11, 2,
            "FOOTNOTE_INLINE_START", yyvsp[-1],
            "error", lasterr
            );
 PyObject_SetAttrString(py_parser, "lasterror", Py_None);
             Py_DECREF(lasterr);
             Py_INCREF(Py_None);
             yyclearin;
        }
#line 4902 "tmp.tab.c"
    break;

  case 152:
#line 2152 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "hyperref_start", 0, 1,
            "LINK_START", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4920 "tmp.tab.c"
    break;

  case 153:
#line 2166 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "hyperref_start", 1, 1,
            "IMG_START", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4938 "tmp.tab.c"
    break;

  case 154:
#line 2183 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "math", 0, 3,
            "MATHBLOCK_START", yyvsp[-2],
            "mathblock_text", yyvsp[-1],
            "MATH_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4958 "tmp.tab.c"
    break;

  case 155:
#line 2199 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "math", 1, 3,
            "MATHINLINE_START", yyvsp[-2],
            "mathblock_text", yyvsp[-1],
            "MATH_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4978 "tmp.tab.c"
    break;

  case 156:
#line 2218 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "mathblock_text", 0, 1,
            "mathblock_span", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 4996 "tmp.tab.c"
    break;

  case 157:
#line 2232 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "mathblock_text", 1, 2,
            "mathblock_span", yyvsp[-1],
            "mathblock_text", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5015 "tmp.tab.c"
    break;

  case 158:
#line 2247 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "mathblock_text", 2, 3,
            "MATHBLOCK_CURLY_OPEN", yyvsp[-2],
            "mathblock_text", yyvsp[-1],
            "MATHBLOCK_CURLY_CLOSE", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5035 "tmp.tab.c"
    break;

  case 159:
#line 2263 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "mathblock_text", 3, 4,
            "MATHBLOCK_CURLY_OPEN", yyvsp[-3],
            "mathblock_text", yyvsp[-2],
            "MATHBLOCK_CURLY_CLOSE", yyvsp[-1],
            "mathblock_text", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5056 "tmp.tab.c"
    break;

  case 160:
#line 2283 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "mathblock_span", 0, 1,
            "mathblock_string", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5074 "tmp.tab.c"
    break;

  case 161:
#line 2297 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "mathblock_span", 1, 1,
            "mathblock_latex", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5092 "tmp.tab.c"
    break;

  case 162:
#line 2311 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "mathblock_span", 2, 1,
            "MATHBLOCK_VERBATIM_PLACEHOLDER", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5110 "tmp.tab.c"
    break;

  case 163:
#line 2325 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "mathblock_span", 3, 2,
            "MATHBLOCK_CURLY_OPEN", yyvsp[-1],
            "MATHBLOCK_CURLY_CLOSE", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5129 "tmp.tab.c"
    break;

  case 164:
#line 2343 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "mathblock_latex", 0, 1,
            "MATHBLOCK_LATEX_COMMAND", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5147 "tmp.tab.c"
    break;

  case 165:
#line 2357 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "mathblock_latex", 1, 4,
            "mathblock_latex", yyvsp[-3],
            "MATHBLOCK_CURLY_OPEN", yyvsp[-2],
            "mathblock_text", yyvsp[-1],
            "MATHBLOCK_CURLY_CLOSE", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5168 "tmp.tab.c"
    break;

  case 166:
#line 2377 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "codeblock_block", 0, 6,
            "CODEBLOCK_START", yyvsp[-5],
            "CODEBLOCK_STRING_BEFORE", yyvsp[-4],
            "attributes", yyvsp[-3],
            "CODEBLOCK_BR", yyvsp[-2],
            "codeblock_string", yyvsp[-1],
            "CODEBLOCK_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5191 "tmp.tab.c"
    break;

  case 167:
#line 2396 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "codeblock_block", 1, 5,
            "CODEBLOCK_START", yyvsp[-4],
            "CODEBLOCK_STRING_BEFORE", yyvsp[-3],
            "CODEBLOCK_BR", yyvsp[-2],
            "codeblock_string", yyvsp[-1],
            "CODEBLOCK_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5213 "tmp.tab.c"
    break;

  case 168:
#line 2414 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "codeblock_block", 2, 5,
            "CODEBLOCK_START", yyvsp[-4],
            "attributes", yyvsp[-3],
            "CODEBLOCK_BR", yyvsp[-2],
            "codeblock_string", yyvsp[-1],
            "CODEBLOCK_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5235 "tmp.tab.c"
    break;

  case 169:
#line 2432 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "codeblock_block", 3, 4,
            "CODEBLOCK_START", yyvsp[-3],
            "CODEBLOCK_BR", yyvsp[-2],
            "codeblock_string", yyvsp[-1],
            "CODEBLOCK_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5256 "tmp.tab.c"
    break;

  case 170:
#line 2449 "src/luke/parser/compiled/tmp.y"
    {
             yyerrok;
             PyObject* lasterr = PyObject_GetAttrString((PyObject*)py_parser, "lasterror");;
          yyval = (*py_callback)(
            py_parser, "codeblock_block", 4, 2,
            "codeblock_block", yyvsp[-1],
            "error", lasterr
            );
 PyObject_SetAttrString(py_parser, "lasterror", Py_None);
             Py_DECREF(lasterr);
             Py_INCREF(Py_None);
             yyclearin;
        }
#line 5274 "tmp.tab.c"
    break;

  case 171:
#line 2466 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attributes", 0, 3,
            "ATTR_START", yyvsp[-2],
            "attribute_list", yyvsp[-1],
            "ATTR_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5294 "tmp.tab.c"
    break;

  case 172:
#line 2485 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute_list", 0, 1,
            "attribute", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5312 "tmp.tab.c"
    break;

  case 173:
#line 2499 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute_list", 1, 2,
            "attribute_list", yyvsp[-1],
            "attribute", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5331 "tmp.tab.c"
    break;

  case 174:
#line 2514 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute_list", 2, 3,
            "attribute_list", yyvsp[-2],
            "ATTR_COMMA", yyvsp[-1],
            "attribute", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5351 "tmp.tab.c"
    break;

  case 175:
#line 2530 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute_list", 3, 0,
            NULL
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5369 "tmp.tab.c"
    break;

  case 176:
#line 2547 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute", 0, 2,
            "ATTR_HASH", yyvsp[-1],
            "ATTR_WORD", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5388 "tmp.tab.c"
    break;

  case 177:
#line 2562 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute", 1, 2,
            "ATTR_DOT", yyvsp[-1],
            "ATTR_WORD", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5407 "tmp.tab.c"
    break;

  case 178:
#line 2577 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute", 2, 2,
            "ATTR_EXCLAMATION", yyvsp[-1],
            "ATTR_WORD", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5426 "tmp.tab.c"
    break;

  case 179:
#line 2592 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute", 3, 3,
            "attribute_varname", yyvsp[-2],
            "ATTR_EQUAL", yyvsp[-1],
            "ATTR_BOOLEAN", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5446 "tmp.tab.c"
    break;

  case 180:
#line 2608 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute", 4, 3,
            "attribute_varname", yyvsp[-2],
            "ATTR_EQUAL", yyvsp[-1],
            "ATTR_NUMBER", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5466 "tmp.tab.c"
    break;

  case 181:
#line 2624 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute", 5, 3,
            "attribute_varname", yyvsp[-2],
            "ATTR_EQUAL", yyvsp[-1],
            "ATTR_STRING", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5486 "tmp.tab.c"
    break;

  case 182:
#line 2640 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute", 6, 3,
            "attribute_varname", yyvsp[-2],
            "ATTR_EQUAL", yyvsp[-1],
            "ATTR_WORD", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5506 "tmp.tab.c"
    break;

  case 183:
#line 2656 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute", 7, 3,
            "attribute_varname", yyvsp[-2],
            "ATTR_EQUAL", yyvsp[-1],
            "attributes", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5526 "tmp.tab.c"
    break;

  case 184:
#line 2672 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute", 8, 3,
            "attribute_varname", yyvsp[-2],
            "ATTR_EQUAL", yyvsp[-1],
            "ATTR_PLACEHOLDER", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5546 "tmp.tab.c"
    break;

  case 185:
#line 2688 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute", 9, 3,
            "attribute_varname", yyvsp[-2],
            "ATTR_EQUAL", yyvsp[-1],
            "math", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5566 "tmp.tab.c"
    break;

  case 186:
#line 2704 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute", 10, 5,
            "attribute_varname", yyvsp[-4],
            "ATTR_EQUAL", yyvsp[-3],
            "ATTR_INPUT", yyvsp[-2],
            "input", yyvsp[-1],
            "HYPERREF_REF_END", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5588 "tmp.tab.c"
    break;

  case 187:
#line 2722 "src/luke/parser/compiled/tmp.y"
    {
             yyerrok;
             PyObject* lasterr = PyObject_GetAttrString((PyObject*)py_parser, "lasterror");;
          yyval = (*py_callback)(
            py_parser, "attribute", 11, 4,
            "attribute_varname", yyvsp[-3],
            "ATTR_EQUAL", yyvsp[-2],
            "ATTR_INPUT", yyvsp[-1],
            "error", lasterr
            );
 PyObject_SetAttrString(py_parser, "lasterror", Py_None);
             Py_DECREF(lasterr);
             Py_INCREF(Py_None);
             yyclearin;
        }
#line 5608 "tmp.tab.c"
    break;

  case 188:
#line 2738 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute", 12, 1,
            "ATTR_BOOLEAN", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5626 "tmp.tab.c"
    break;

  case 189:
#line 2752 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute", 13, 1,
            "ATTR_NUMBER", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5644 "tmp.tab.c"
    break;

  case 190:
#line 2766 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute", 14, 1,
            "attribute_varname", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5662 "tmp.tab.c"
    break;

  case 191:
#line 2780 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute", 15, 1,
            "ATTR_PLACEHOLDER", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5680 "tmp.tab.c"
    break;

  case 192:
#line 2794 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute", 16, 1,
            "attributes", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5698 "tmp.tab.c"
    break;

  case 193:
#line 2811 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute_varname", 0, 1,
            "ATTR_WORD", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5716 "tmp.tab.c"
    break;

  case 194:
#line 2825 "src/luke/parser/compiled/tmp.y"
    {
          yyval = (*py_callback)(
            py_parser, "attribute_varname", 1, 1,
            "ATTR_STRING", yyvsp[0]
            );
          {
            PyObject* obj = PyErr_Occurred();
            if (obj) {
              //yyerror(&yylloc, "exception raised");
              YYERROR;
            }
          }
        }
#line 5734 "tmp.tab.c"
    break;


#line 5738 "tmp.tab.c"

      default: break;
    }
  /* User semantic actions sometimes alter yychar, and that requires
     that yytoken be updated with the new translation.  We take the
     approach of translating immediately before every use of yytoken.
     One alternative is translating here after every semantic action,
     but that translation would be missed if the semantic action invokes
     YYABORT, YYACCEPT, or YYERROR immediately after altering yychar or
     if it invokes YYBACKUP.  In the case of YYABORT or YYACCEPT, an
     incorrect destructor might then be invoked immediately.  In the
     case of YYERROR or YYBACKUP, subsequent parser actions might lead
     to an incorrect destructor call or verbose syntax error message
     before the lookahead is translated.  */
  YY_SYMBOL_PRINT ("-> $$ =", yyr1[yyn], &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);

  *++yyvsp = yyval;
  *++yylsp = yyloc;

  /* Now 'shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */
  {
    const int yylhs = yyr1[yyn] - YYNTOKENS;
    const int yyi = yypgoto[yylhs] + *yyssp;
    yystate = (0 <= yyi && yyi <= YYLAST && yycheck[yyi] == *yyssp
               ? yytable[yyi]
               : yydefgoto[yylhs]);
  }

  goto yynewstate;


/*--------------------------------------.
| yyerrlab -- here on detecting error.  |
`--------------------------------------*/
yyerrlab:
  /* Make sure we have latest lookahead translation.  See comments at
     user semantic actions for why this is necessary.  */
  yytoken = yychar == YYEMPTY ? YYEMPTY : YYTRANSLATE (yychar);

  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
#if ! YYERROR_VERBOSE
      yyerror (&yylloc, scanner, YY_("syntax error"));
#else
# define YYSYNTAX_ERROR yysyntax_error (&yymsg_alloc, &yymsg, \
                                        yyssp, yytoken)
      {
        char const *yymsgp = YY_("syntax error");
        int yysyntax_error_status;
        yysyntax_error_status = YYSYNTAX_ERROR;
        if (yysyntax_error_status == 0)
          yymsgp = yymsg;
        else if (yysyntax_error_status == 1)
          {
            if (yymsg != yymsgbuf)
              YYSTACK_FREE (yymsg);
            yymsg = (char *) YYSTACK_ALLOC (yymsg_alloc);
            if (!yymsg)
              {
                yymsg = yymsgbuf;
                yymsg_alloc = sizeof yymsgbuf;
                yysyntax_error_status = 2;
              }
            else
              {
                yysyntax_error_status = YYSYNTAX_ERROR;
                yymsgp = yymsg;
              }
          }
        yyerror (&yylloc, scanner, yymsgp);
        if (yysyntax_error_status == 2)
          goto yyexhaustedlab;
      }
# undef YYSYNTAX_ERROR
#endif
    }

  yyerror_range[1] = yylloc;

  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
         error, discard it.  */

      if (yychar <= YYEOF)
        {
          /* Return failure if at end of input.  */
          if (yychar == YYEOF)
            YYABORT;
        }
      else
        {
          yydestruct ("Error: discarding",
                      yytoken, &yylval, &yylloc, scanner);
          yychar = YYEMPTY;
        }
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:
  /* Pacify compilers when the user code never invokes YYERROR and the
     label yyerrorlab therefore never appears in user code.  */
  if (0)
    YYERROR;

  /* Do not reclaim the symbols of the rule whose action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;      /* Each real token shifted decrements this.  */

  for (;;)
    {
      yyn = yypact[yystate];
      if (!yypact_value_is_default (yyn))
        {
          yyn += YYTERROR;
          if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYTERROR)
            {
              yyn = yytable[yyn];
              if (0 < yyn)
                break;
            }
        }

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
        YYABORT;

      yyerror_range[1] = *yylsp;
      yydestruct ("Error: popping",
                  yystos[yystate], yyvsp, yylsp, scanner);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END

  yyerror_range[2] = yylloc;
  /* Using YYLLOC is tempting, but would change the location of
     the lookahead.  YYLOC is available though.  */
  YYLLOC_DEFAULT (yyloc, yyerror_range, 2);
  *++yylsp = yyloc;

  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", yystos[yyn], yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturn;


/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturn;


#if !defined yyoverflow || YYERROR_VERBOSE
/*-------------------------------------------------.
| yyexhaustedlab -- memory exhaustion comes here.  |
`-------------------------------------------------*/
yyexhaustedlab:
  yyerror (&yylloc, scanner, YY_("memory exhausted"));
  yyresult = 2;
  /* Fall through.  */
#endif


/*-----------------------------------------------------.
| yyreturn -- parsing is finished, return the result.  |
`-----------------------------------------------------*/
yyreturn:
  if (yychar != YYEMPTY)
    {
      /* Make sure we have latest lookahead translation.  See comments at
         user semantic actions for why this is necessary.  */
      yytoken = YYTRANSLATE (yychar);
      yydestruct ("Cleanup: discarding lookahead",
                  yytoken, &yylval, &yylloc, scanner);
    }
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
                  yystos[*yyssp], yyvsp, yylsp, scanner);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif
  yyps->yynew = 1;


/*-----------------------------------------.
| yypushreturn -- ask for the next token.  |
`-----------------------------------------*/
yypushreturn:
#if YYERROR_VERBOSE
  if (yymsg != yymsgbuf)
    YYSTACK_FREE (yymsg);
#endif
  return yyresult;
}
#line 2842 "src/luke/parser/compiled/tmp.y"


__attribute__ ((dllexport)) void do_parse(void *parser1,
              void *(*cb)(void *, char *, int, int, ...),
              void (*in)(void *, char*, int *, int),
              int debug
              )
{
   py_callback = cb;
   py_input = in;
   py_parser = parser1;
   yydebug = debug; // For Bison (still global, even in a reentrant parser)
yyscan_t scanner;
yylex_init(&scanner);
if (debug) yyset_debug(1, scanner); // For Flex (no longer a global, but rather a member of yyguts_t)


int status;
yypstate *ps = yypstate_new ();
YYSTYPE pushed_value;
YYLTYPE yylloc;
yylloc.first_line = yylloc.first_column = yylloc.last_line = yylloc.last_column = 1;
do {
  int token = yylex(&pushed_value,&yylloc, scanner);
  status = yypush_parse (ps, token , &pushed_value, &yylloc, scanner);
} while (status == YYPUSH_MORE);
yypstate_delete(ps);
yylex_destroy(scanner);return;
}


void yyerror(YYLTYPE *locp, yyscan_t scanner, char const *msg) {

  PyObject *error = PyErr_Occurred();
  if(error) PyErr_Clear();
  PyObject *fn = PyObject_GetAttrString((PyObject *)py_parser,
                                        "report_syntax_error");
  if (!fn)
      return;

  PyObject *args;
  args = Py_BuildValue("(s,s,i,i,i,i)", msg, yyget_text(scanner),
                       locp->first_line, locp->first_column,
                       locp->last_line, locp->last_column);

  if (!args)
      return;


  PyObject *res = PyObject_CallObject(fn, args);
  Py_DECREF(args);

  if (!res)
      return;

  Py_XDECREF(res);
  return;
}
