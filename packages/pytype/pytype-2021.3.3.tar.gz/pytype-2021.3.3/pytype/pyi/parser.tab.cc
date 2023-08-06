// A Bison parser, made by GNU Bison 3.7.5.

// Skeleton implementation for Bison LALR(1) parsers in C++

// Copyright (C) 2002-2015, 2018-2021 Free Software Foundation, Inc.

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

// As a special exception, you may create a larger work that contains
// part or all of the Bison parser skeleton and distribute that work
// under terms of your choice, so long as that work isn't itself a
// parser generator using the skeleton or a modified version thereof
// as a parser skeleton.  Alternatively, if you modify or redistribute
// the parser skeleton itself, you may (at your option) remove this
// special exception, which will cause the skeleton and the resulting
// Bison output files to be licensed under the GNU General Public
// License without this special exception.

// This special exception was added by the Free Software Foundation in
// version 2.2 of Bison.

// DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
// especially those whose name start with YY_ or yy_.  They are
// private implementation details that can be changed or removed.


// Take the name prefix into account.
#define yylex   pytypelex



#include "parser.tab.hh"


// Unqualified %code blocks.
#line 34 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"

namespace {
PyObject* DOT_STRING = PyString_FromString(".");

/* Helper functions for building up lists. */
PyObject* StartList(PyObject* item);
PyObject* AppendList(PyObject* list, PyObject* item);
PyObject* ExtendList(PyObject* dst, PyObject* src);

}  // end namespace


// Check that a python value is not NULL.  This must be a macro because it
// calls YYERROR (which is a goto).
#define CHECK(x, loc) do { if (x == NULL) {\
    ctx->SetErrorLocation(loc); \
    YYERROR; \
  }} while(0)

// pytypelex is generated in lexer.lex.cc, but because it uses semantic_type and
// location, it must be declared here.
int pytypelex(pytype::parser::semantic_type* lvalp, pytype::location* llocp,
              void* scanner);


#line 74 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"


#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> // FIXME: INFRINGES ON USER NAME SPACE.
#   define YY_(msgid) dgettext ("bison-runtime", msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(msgid) msgid
# endif
#endif


// Whether we are compiled with exception support.
#ifndef YY_EXCEPTIONS
# if defined __GNUC__ && !defined __EXCEPTIONS
#  define YY_EXCEPTIONS 0
# else
#  define YY_EXCEPTIONS 1
# endif
#endif

#define YYRHSLOC(Rhs, K) ((Rhs)[K].location)
/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

# ifndef YYLLOC_DEFAULT
#  define YYLLOC_DEFAULT(Current, Rhs, N)                               \
    do                                                                  \
      if (N)                                                            \
        {                                                               \
          (Current).begin  = YYRHSLOC (Rhs, 1).begin;                   \
          (Current).end    = YYRHSLOC (Rhs, N).end;                     \
        }                                                               \
      else                                                              \
        {                                                               \
          (Current).begin = (Current).end = YYRHSLOC (Rhs, 0).end;      \
        }                                                               \
    while (false)
# endif


// Enable debugging if requested.
#if PYTYPEDEBUG

// A pseudo ostream that takes yydebug_ into account.
# define YYCDEBUG if (yydebug_) (*yycdebug_)

# define YY_SYMBOL_PRINT(Title, Symbol)         \
  do {                                          \
    if (yydebug_)                               \
    {                                           \
      *yycdebug_ << Title << ' ';               \
      yy_print_ (*yycdebug_, Symbol);           \
      *yycdebug_ << '\n';                       \
    }                                           \
  } while (false)

# define YY_REDUCE_PRINT(Rule)          \
  do {                                  \
    if (yydebug_)                       \
      yy_reduce_print_ (Rule);          \
  } while (false)

# define YY_STACK_PRINT()               \
  do {                                  \
    if (yydebug_)                       \
      yy_stack_print_ ();                \
  } while (false)

#else // !PYTYPEDEBUG

# define YYCDEBUG if (false) std::cerr
# define YY_SYMBOL_PRINT(Title, Symbol)  YY_USE (Symbol)
# define YY_REDUCE_PRINT(Rule)           static_cast<void> (0)
# define YY_STACK_PRINT()                static_cast<void> (0)

#endif // !PYTYPEDEBUG

#define yyerrok         (yyerrstatus_ = 0)
#define yyclearin       (yyla.clear ())

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab
#define YYRECOVERING()  (!!yyerrstatus_)

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
namespace pytype {
#line 167 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"

  /// Build a parser object.
  parser::parser (void* scanner_yyarg, pytype::Context* ctx_yyarg)
#if PYTYPEDEBUG
    : yydebug_ (false),
      yycdebug_ (&std::cerr),
#else
    :
#endif
      scanner (scanner_yyarg),
      ctx (ctx_yyarg)
  {}

  parser::~parser ()
  {}

  parser::syntax_error::~syntax_error () YY_NOEXCEPT YY_NOTHROW
  {}

  /*---------------.
  | symbol kinds.  |
  `---------------*/

  // basic_symbol.
  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (const basic_symbol& that)
    : Base (that)
    , value (that.value)
    , location (that.location)
  {}


  /// Constructor for valueless symbols.
  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, YY_MOVE_REF (location_type) l)
    : Base (t)
    , value ()
    , location (l)
  {}

  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, YY_RVREF (semantic_type) v, YY_RVREF (location_type) l)
    : Base (t)
    , value (YY_MOVE (v))
    , location (YY_MOVE (l))
  {}

  template <typename Base>
  parser::symbol_kind_type
  parser::basic_symbol<Base>::type_get () const YY_NOEXCEPT
  {
    return this->kind ();
  }

  template <typename Base>
  bool
  parser::basic_symbol<Base>::empty () const YY_NOEXCEPT
  {
    return this->kind () == symbol_kind::S_YYEMPTY;
  }

  template <typename Base>
  void
  parser::basic_symbol<Base>::move (basic_symbol& s)
  {
    super_type::move (s);
    value = YY_MOVE (s.value);
    location = YY_MOVE (s.location);
  }

  // by_kind.
  parser::by_kind::by_kind ()
    : kind_ (symbol_kind::S_YYEMPTY)
  {}

#if 201103L <= YY_CPLUSPLUS
  parser::by_kind::by_kind (by_kind&& that)
    : kind_ (that.kind_)
  {
    that.clear ();
  }
#endif

  parser::by_kind::by_kind (const by_kind& that)
    : kind_ (that.kind_)
  {}

  parser::by_kind::by_kind (token_kind_type t)
    : kind_ (yytranslate_ (t))
  {}

  void
  parser::by_kind::clear () YY_NOEXCEPT
  {
    kind_ = symbol_kind::S_YYEMPTY;
  }

  void
  parser::by_kind::move (by_kind& that)
  {
    kind_ = that.kind_;
    that.clear ();
  }

  parser::symbol_kind_type
  parser::by_kind::kind () const YY_NOEXCEPT
  {
    return kind_;
  }

  parser::symbol_kind_type
  parser::by_kind::type_get () const YY_NOEXCEPT
  {
    return this->kind ();
  }


  // by_state.
  parser::by_state::by_state () YY_NOEXCEPT
    : state (empty_state)
  {}

  parser::by_state::by_state (const by_state& that) YY_NOEXCEPT
    : state (that.state)
  {}

  void
  parser::by_state::clear () YY_NOEXCEPT
  {
    state = empty_state;
  }

  void
  parser::by_state::move (by_state& that)
  {
    state = that.state;
    that.clear ();
  }

  parser::by_state::by_state (state_type s) YY_NOEXCEPT
    : state (s)
  {}

  parser::symbol_kind_type
  parser::by_state::kind () const YY_NOEXCEPT
  {
    if (state == empty_state)
      return symbol_kind::S_YYEMPTY;
    else
      return YY_CAST (symbol_kind_type, yystos_[+state]);
  }

  parser::stack_symbol_type::stack_symbol_type ()
  {}

  parser::stack_symbol_type::stack_symbol_type (YY_RVREF (stack_symbol_type) that)
    : super_type (YY_MOVE (that.state), YY_MOVE (that.value), YY_MOVE (that.location))
  {
#if 201103L <= YY_CPLUSPLUS
    // that is emptied.
    that.state = empty_state;
#endif
  }

  parser::stack_symbol_type::stack_symbol_type (state_type s, YY_MOVE_REF (symbol_type) that)
    : super_type (s, YY_MOVE (that.value), YY_MOVE (that.location))
  {
    // that is emptied.
    that.kind_ = symbol_kind::S_YYEMPTY;
  }

#if YY_CPLUSPLUS < 201103L
  parser::stack_symbol_type&
  parser::stack_symbol_type::operator= (const stack_symbol_type& that)
  {
    state = that.state;
    value = that.value;
    location = that.location;
    return *this;
  }

  parser::stack_symbol_type&
  parser::stack_symbol_type::operator= (stack_symbol_type& that)
  {
    state = that.state;
    value = that.value;
    location = that.location;
    // that is emptied.
    that.state = empty_state;
    return *this;
  }
#endif

  template <typename Base>
  void
  parser::yy_destroy_ (const char* yymsg, basic_symbol<Base>& yysym) const
  {
    if (yymsg)
      YY_SYMBOL_PRINT (yymsg, yysym);

    // User destructor.
    switch (yysym.kind ())
    {
      case symbol_kind::S_NAME: // NAME
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 374 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_NUMBER: // NUMBER
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 380 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_STRING: // STRING
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 386 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_LEXERROR: // LEXERROR
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 392 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_start: // start
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 398 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_unit: // unit
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 404 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_alldefs: // alldefs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 410 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_classdef: // classdef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 416 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_class_name: // class_name
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 422 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_parents: // parents
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 428 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_parent_list: // parent_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 434 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_parent: // parent
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 440 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_class_funcs: // maybe_class_funcs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 446 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_class_funcs: // class_funcs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 452 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_funcdefs: // funcdefs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 458 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_if_stmt: // if_stmt
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 464 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_if_and_elifs: // if_and_elifs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 470 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_class_if_stmt: // class_if_stmt
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 476 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_class_if_and_elifs: // class_if_and_elifs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 482 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_if_cond: // if_cond
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 488 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_elif_cond: // elif_cond
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 494 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_else_cond: // else_cond
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 500 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_condition: // condition
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 506 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_version_tuple: // version_tuple
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 512 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_condition_op: // condition_op
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.str)); }
#line 518 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_constantdef: // constantdef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 524 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_importdef: // importdef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 530 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_import_items: // import_items
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 536 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_import_item: // import_item
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 542 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_import_name: // import_name
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 548 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_from_list: // from_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 554 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_from_items: // from_items
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 560 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_from_item: // from_item
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 566 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_alias_or_constant: // alias_or_constant
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 572 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_string_list: // maybe_string_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 578 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_string_list: // string_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 584 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typevardef: // typevardef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 590 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typevar_args: // typevar_args
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 596 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typevar_kwargs: // typevar_kwargs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 602 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typevar_kwarg: // typevar_kwarg
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 608 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_funcdef: // funcdef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 614 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_funcname: // funcname
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 620 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_decorators: // decorators
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 626 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_decorator: // decorator
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 632 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_async: // maybe_async
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 638 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_params: // params
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 644 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_param_list: // param_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 650 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_param: // param
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 656 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_param_type: // param_type
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 662 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_param_default: // param_default
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 668 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_param_star_name: // param_star_name
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 674 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_return: // return
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 680 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_body: // maybe_body
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 686 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_body: // body
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 692 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_body_stmt: // body_stmt
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 698 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_type_parameters: // type_parameters
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 704 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_type_parameter: // type_parameter
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 710 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_type_list: // maybe_type_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 716 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_type_list: // type_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 722 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_type: // type
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 728 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_named_tuple_fields: // named_tuple_fields
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 734 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_named_tuple_field_list: // named_tuple_field_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 740 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_named_tuple_field: // named_tuple_field
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 746 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_coll_named_tuple_fields: // coll_named_tuple_fields
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 752 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_coll_named_tuple_field_list: // coll_named_tuple_field_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 758 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_coll_named_tuple_field: // coll_named_tuple_field
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 764 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typed_dict_fields: // typed_dict_fields
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 770 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typed_dict_field_dict: // typed_dict_field_dict
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 776 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_typed_dict_field: // typed_dict_field
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 782 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_typed_dict_kwarg: // maybe_typed_dict_kwarg
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 788 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_type_tuple_elements: // type_tuple_elements
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 794 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_type_tuple_literal: // type_tuple_literal
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 800 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_dotted_name: // dotted_name
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 806 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_getitem_key: // getitem_key
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 812 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case symbol_kind::S_maybe_number: // maybe_number
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 818 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      default:
        break;
    }
  }

#if PYTYPEDEBUG
  template <typename Base>
  void
  parser::yy_print_ (std::ostream& yyo, const basic_symbol<Base>& yysym) const
  {
    std::ostream& yyoutput = yyo;
    YY_USE (yyoutput);
    if (yysym.empty ())
      yyo << "empty symbol";
    else
      {
        symbol_kind_type yykind = yysym.kind ();
        yyo << (yykind < YYNTOKENS ? "token" : "nterm")
            << ' ' << yysym.name () << " ("
            << yysym.location << ": ";
        YY_USE (yykind);
        yyo << ')';
      }
  }
#endif

  void
  parser::yypush_ (const char* m, YY_MOVE_REF (stack_symbol_type) sym)
  {
    if (m)
      YY_SYMBOL_PRINT (m, sym);
    yystack_.push (YY_MOVE (sym));
  }

  void
  parser::yypush_ (const char* m, state_type s, YY_MOVE_REF (symbol_type) sym)
  {
#if 201103L <= YY_CPLUSPLUS
    yypush_ (m, stack_symbol_type (s, std::move (sym)));
#else
    stack_symbol_type ss (s, sym);
    yypush_ (m, ss);
#endif
  }

  void
  parser::yypop_ (int n)
  {
    yystack_.pop (n);
  }

#if PYTYPEDEBUG
  std::ostream&
  parser::debug_stream () const
  {
    return *yycdebug_;
  }

  void
  parser::set_debug_stream (std::ostream& o)
  {
    yycdebug_ = &o;
  }


  parser::debug_level_type
  parser::debug_level () const
  {
    return yydebug_;
  }

  void
  parser::set_debug_level (debug_level_type l)
  {
    yydebug_ = l;
  }
#endif // PYTYPEDEBUG

  parser::state_type
  parser::yy_lr_goto_state_ (state_type yystate, int yysym)
  {
    int yyr = yypgoto_[yysym - YYNTOKENS] + yystate;
    if (0 <= yyr && yyr <= yylast_ && yycheck_[yyr] == yystate)
      return yytable_[yyr];
    else
      return yydefgoto_[yysym - YYNTOKENS];
  }

  bool
  parser::yy_pact_value_is_default_ (int yyvalue)
  {
    return yyvalue == yypact_ninf_;
  }

  bool
  parser::yy_table_value_is_error_ (int yyvalue)
  {
    return yyvalue == yytable_ninf_;
  }

  int
  parser::operator() ()
  {
    return parse ();
  }

  int
  parser::parse ()
  {
    int yyn;
    /// Length of the RHS of the rule being reduced.
    int yylen = 0;

    // Error handling.
    int yynerrs_ = 0;
    int yyerrstatus_ = 0;

    /// The lookahead symbol.
    symbol_type yyla;

    /// The locations where the error started and ended.
    stack_symbol_type yyerror_range[3];

    /// The return value of parse ().
    int yyresult;

#if YY_EXCEPTIONS
    try
#endif // YY_EXCEPTIONS
      {
    YYCDEBUG << "Starting parse\n";


    /* Initialize the stack.  The initial state will be set in
       yynewstate, since the latter expects the semantical and the
       location values to have been already stored, initialize these
       stacks with a primary value.  */
    yystack_.clear ();
    yypush_ (YY_NULLPTR, 0, YY_MOVE (yyla));

  /*-----------------------------------------------.
  | yynewstate -- push a new symbol on the stack.  |
  `-----------------------------------------------*/
  yynewstate:
    YYCDEBUG << "Entering state " << int (yystack_[0].state) << '\n';
    YY_STACK_PRINT ();

    // Accept?
    if (yystack_[0].state == yyfinal_)
      YYACCEPT;

    goto yybackup;


  /*-----------.
  | yybackup.  |
  `-----------*/
  yybackup:
    // Try to take a decision without lookahead.
    yyn = yypact_[+yystack_[0].state];
    if (yy_pact_value_is_default_ (yyn))
      goto yydefault;

    // Read a lookahead token.
    if (yyla.empty ())
      {
        YYCDEBUG << "Reading a token\n";
#if YY_EXCEPTIONS
        try
#endif // YY_EXCEPTIONS
          {
            yyla.kind_ = yytranslate_ (yylex (&yyla.value, &yyla.location, scanner));
          }
#if YY_EXCEPTIONS
        catch (const syntax_error& yyexc)
          {
            YYCDEBUG << "Caught exception: " << yyexc.what() << '\n';
            error (yyexc);
            goto yyerrlab1;
          }
#endif // YY_EXCEPTIONS
      }
    YY_SYMBOL_PRINT ("Next token is", yyla);

    if (yyla.kind () == symbol_kind::S_YYerror)
    {
      // The scanner already issued an error message, process directly
      // to error recovery.  But do not keep the error token as
      // lookahead, it is too special and may lead us to an endless
      // loop in error recovery. */
      yyla.kind_ = symbol_kind::S_YYUNDEF;
      goto yyerrlab1;
    }

    /* If the proper action on seeing token YYLA.TYPE is to reduce or
       to detect an error, take that action.  */
    yyn += yyla.kind ();
    if (yyn < 0 || yylast_ < yyn || yycheck_[yyn] != yyla.kind ())
      {
        goto yydefault;
      }

    // Reduce or error.
    yyn = yytable_[yyn];
    if (yyn <= 0)
      {
        if (yy_table_value_is_error_ (yyn))
          goto yyerrlab;
        yyn = -yyn;
        goto yyreduce;
      }

    // Count tokens shifted since error; after three, turn off error status.
    if (yyerrstatus_)
      --yyerrstatus_;

    // Shift the lookahead token.
    yypush_ ("Shifting", state_type (yyn), YY_MOVE (yyla));
    goto yynewstate;


  /*-----------------------------------------------------------.
  | yydefault -- do the default action for the current state.  |
  `-----------------------------------------------------------*/
  yydefault:
    yyn = yydefact_[+yystack_[0].state];
    if (yyn == 0)
      goto yyerrlab;
    goto yyreduce;


  /*-----------------------------.
  | yyreduce -- do a reduction.  |
  `-----------------------------*/
  yyreduce:
    yylen = yyr2_[yyn];
    {
      stack_symbol_type yylhs;
      yylhs.state = yy_lr_goto_state_ (yystack_[yylen].state, yyr1_[yyn]);
      /* If YYLEN is nonzero, implement the default value of the
         action: '$$ = $1'.  Otherwise, use the top of the stack.

         Otherwise, the following line sets YYLHS.VALUE to garbage.
         This behavior is undocumented and Bison users should not rely
         upon it.  */
      if (yylen)
        yylhs.value = yystack_[yylen - 1].value;
      else
        yylhs.value = yystack_[0].value;

      // Default location.
      {
        stack_type::slice range (yystack_, yylen);
        YYLLOC_DEFAULT (yylhs.location, range, yylen);
        yyerror_range[1].location = yylhs.location;
      }

      // Perform the reduction.
      YY_REDUCE_PRINT (yyn);
#if YY_EXCEPTIONS
      try
#endif // YY_EXCEPTIONS
        {
          switch (yyn)
            {
  case 2: // start: unit "end of file"
#line 135 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1089 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 3: // start: TRIPLEQUOTED unit "end of file"
#line 136 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                          { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1095 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 4: // unit: alldefs
#line 140 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1101 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 5: // alldefs: alldefs constantdef
#line 144 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                        { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1107 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 6: // alldefs: alldefs funcdef
#line 145 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1113 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 7: // alldefs: alldefs importdef
#line 146 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1119 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 8: // alldefs: alldefs alias_or_constant
#line 147 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                              {
      (yylhs.value.obj) = (yystack_[1].value.obj);
      PyObject* tmp = ctx->Call(kAddAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
    }
#line 1130 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 9: // alldefs: alldefs classdef
#line 153 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1136 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 10: // alldefs: alldefs typevardef
#line 154 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1142 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 11: // alldefs: alldefs if_stmt
#line 155 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1152 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 12: // alldefs: %empty
#line 160 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyList_New(0); }
#line 1158 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 15: // classdef: decorators CLASS class_name parents ':' maybe_type_ignore maybe_class_funcs
#line 173 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewClass, "(NNNN)", (yystack_[6].value.obj), (yystack_[4].value.obj), (yystack_[3].value.obj), (yystack_[0].value.obj));
      // Fix location tracking. See funcdef.
      yylhs.location.begin = yystack_[4].location.begin;
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1169 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 16: // classdef: decorators CLASS NAMEDTUPLE parents ':' maybe_type_ignore maybe_class_funcs
#line 180 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewClass, "(NNNN)", (yystack_[6].value.obj), PyString_FromString("NamedTuple"), (yystack_[3].value.obj), (yystack_[0].value.obj));
      // Fix location tracking. See funcdef.
      yylhs.location.begin = yystack_[4].location.begin;
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1180 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 17: // class_name: NAME
#line 189 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         {
      // Do not borrow the $1 reference since it is also returned later
      // in $$.  Use O instead of N in the format string.
      PyObject* tmp = ctx->Call(kRegisterClassName, "(O)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
      (yylhs.value.obj) = (yystack_[0].value.obj);
    }
#line 1193 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 18: // parents: '(' parent_list ')'
#line 200 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                        { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1199 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 19: // parents: '(' ')'
#line 201 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyList_New(0); }
#line 1205 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 20: // parents: %empty
#line 202 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = PyList_New(0); }
#line 1211 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 21: // parent_list: parent_list ',' parent
#line 206 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1217 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 22: // parent_list: parent
#line 207 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1223 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 23: // parent: type
#line 211 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1229 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 24: // parent: NAME '=' type
#line 212 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1235 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 25: // parent: NAMEDTUPLE
#line 213 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = PyString_FromString("NamedTuple"); }
#line 1241 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 26: // parent: TYPEDDICT
#line 214 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              {
      (yylhs.value.obj) = ctx->Call(kNewType, "(N)", PyString_FromString("TypedDict"));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1250 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 27: // maybe_class_funcs: pass_or_ellipsis maybe_type_ignore
#line 221 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                       { (yylhs.value.obj) = PyList_New(0); }
#line 1256 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 28: // maybe_class_funcs: INDENT class_funcs DEDENT
#line 222 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                              { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1262 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 29: // maybe_class_funcs: INDENT TRIPLEQUOTED class_funcs DEDENT
#line 223 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                           { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1268 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 30: // class_funcs: pass_or_ellipsis
#line 227 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { (yylhs.value.obj) = PyList_New(0); }
#line 1274 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 31: // class_funcs: funcdefs
#line 228 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1280 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 32: // funcdefs: funcdefs constantdef
#line 232 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                         { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1286 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 33: // funcdefs: funcdefs alias_or_constant
#line 233 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                               {
      PyObject* tmp = ctx->Call(kNewAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      (yylhs.value.obj) = AppendList((yystack_[1].value.obj), tmp);
    }
#line 1296 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 34: // funcdefs: funcdefs funcdef
#line 238 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1302 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 35: // funcdefs: funcdefs class_if_stmt
#line 239 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1312 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 36: // funcdefs: funcdefs classdef
#line 244 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1318 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 37: // funcdefs: %empty
#line 245 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1324 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 38: // if_stmt: if_and_elifs else_cond ':' INDENT alldefs DEDENT
#line 250 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                     {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1332 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 39: // if_stmt: if_and_elifs
#line 253 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1338 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 40: // if_and_elifs: if_cond ':' INDENT alldefs DEDENT
#line 258 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                      {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1346 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 41: // if_and_elifs: if_and_elifs elif_cond ':' INDENT alldefs DEDENT
#line 262 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                     {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1354 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 42: // class_if_stmt: class_if_and_elifs else_cond ':' INDENT funcdefs DEDENT
#line 275 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                            {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1362 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 43: // class_if_stmt: class_if_and_elifs
#line 278 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1368 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 44: // class_if_and_elifs: if_cond ':' INDENT funcdefs DEDENT
#line 283 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                       {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1376 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 45: // class_if_and_elifs: class_if_and_elifs elif_cond ':' INDENT funcdefs DEDENT
#line 287 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                            {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1384 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 46: // if_cond: IF condition
#line 299 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = ctx->Call(kIfBegin, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1390 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 47: // elif_cond: ELIF condition
#line 303 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                   { (yylhs.value.obj) = ctx->Call(kIfElif, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1396 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 48: // else_cond: ELSE
#line 307 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = ctx->Call(kIfElse, "()"); CHECK((yylhs.value.obj), yylhs.location); }
#line 1402 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 49: // condition: dotted_name condition_op STRING
#line 311 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                    {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1410 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 50: // condition: dotted_name condition_op version_tuple
#line 314 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                           {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1418 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 51: // condition: dotted_name '[' getitem_key ']' condition_op NUMBER
#line 317 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                        {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1426 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 52: // condition: dotted_name '[' getitem_key ']' condition_op version_tuple
#line 320 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                               {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1434 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 53: // condition: condition AND condition
#line 323 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                            { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "and", (yystack_[0].value.obj)); }
#line 1440 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 54: // condition: condition OR condition
#line 324 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "or", (yystack_[0].value.obj)); }
#line 1446 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 55: // condition: '(' condition ')'
#line 325 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1452 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 56: // version_tuple: '(' NUMBER ',' ')'
#line 329 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = Py_BuildValue("(N)", (yystack_[2].value.obj)); }
#line 1458 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 57: // version_tuple: '(' NUMBER ',' NUMBER ')'
#line 330 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                              { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj)); }
#line 1464 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 58: // version_tuple: '(' NUMBER ',' NUMBER ',' NUMBER ')'
#line 331 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                         {
      (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj));
    }
#line 1472 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 59: // condition_op: '<'
#line 337 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "<"; }
#line 1478 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 60: // condition_op: '>'
#line 338 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = ">"; }
#line 1484 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 61: // condition_op: LE
#line 339 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "<="; }
#line 1490 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 62: // condition_op: GE
#line 340 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = ">="; }
#line 1496 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 63: // condition_op: EQ
#line 341 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "=="; }
#line 1502 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 64: // condition_op: NE
#line 342 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "!="; }
#line 1508 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 65: // constantdef: NAME '=' NUMBER
#line 346 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1517 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 66: // constantdef: NAME '=' STRING
#line 350 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1526 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 67: // constantdef: NAME '=' type_tuple_literal
#line 354 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1535 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 68: // constantdef: NAME '=' ELLIPSIS
#line 358 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), ctx->Value(kAnything));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1544 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 69: // constantdef: NAME '=' ELLIPSIS TYPECOMMENT type maybe_type_ignore
#line 362 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                         {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1553 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 70: // constantdef: NAME ':' type maybe_type_ignore
#line 366 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1562 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 71: // constantdef: NAME ':' type '=' ELLIPSIS maybe_type_ignore
#line 370 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                 {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[3].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1571 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 72: // constantdef: TYPEDDICT ':' type maybe_type_ignore
#line 374 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                         {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", PyString_FromString("TypedDict"), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1580 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 73: // constantdef: TYPEDDICT ':' type '=' ELLIPSIS maybe_type_ignore
#line 378 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                      {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", PyString_FromString("TypedDict"), (yystack_[3].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1589 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 74: // importdef: IMPORT import_items maybe_type_ignore
#line 385 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                          {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(ON)", Py_None, (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1598 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 75: // importdef: FROM import_name IMPORT from_list maybe_type_ignore
#line 389 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                        {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1607 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 76: // importdef: FROM '.' IMPORT from_list maybe_type_ignore
#line 393 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                {
      // Special-case "from . import" and pass in a __PACKAGE__ token that
      // the Python parser code will rewrite to the current package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PACKAGE__", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1618 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 77: // importdef: FROM '.' '.' IMPORT from_list maybe_type_ignore
#line 399 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                    {
      // Special-case "from .. import" and pass in a __PARENT__ token that
      // the Python parser code will rewrite to the parent package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PARENT__", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1629 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 78: // import_items: import_items ',' import_item
#line 408 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                 { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1635 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 79: // import_items: import_item
#line 409 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1641 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 80: // import_item: dotted_name
#line 413 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1647 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 81: // import_item: dotted_name AS NAME
#line 414 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                        { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1653 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 82: // import_name: dotted_name
#line 419 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1659 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 83: // import_name: '.' import_name
#line 420 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = PyString_FromFormat(".%s", PyString_AsString((yystack_[0].value.obj)));
      Py_DECREF((yystack_[0].value.obj));
    }
#line 1668 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 84: // from_list: from_items
#line 427 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1674 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 85: // from_list: '(' from_items ')'
#line 428 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1680 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 86: // from_list: '(' from_items ',' ')'
#line 429 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 1686 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 87: // from_items: from_items ',' from_item
#line 433 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                             { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1692 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 88: // from_items: from_item
#line 434 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1698 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 89: // from_item: NAME
#line 438 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1704 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 90: // from_item: NAMEDTUPLE
#line 439 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               {
      (yylhs.value.obj) = PyString_FromString("NamedTuple");
    }
#line 1712 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 91: // from_item: COLL_NAMEDTUPLE
#line 442 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = PyString_FromString("namedtuple");
    }
#line 1720 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 92: // from_item: NEWTYPE
#line 445 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            {
      (yylhs.value.obj) = PyString_FromString("NewType");
    }
#line 1728 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 93: // from_item: TYPEDDICT
#line 448 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              {
      (yylhs.value.obj) = PyString_FromString("TypedDict");
    }
#line 1736 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 94: // from_item: TYPEVAR
#line 451 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            {
      (yylhs.value.obj) = PyString_FromString("TypeVar");
    }
#line 1744 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 95: // from_item: '*'
#line 454 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        {
      (yylhs.value.obj) = PyString_FromString("*");
    }
#line 1752 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 96: // from_item: NAME AS NAME
#line 457 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1758 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 97: // from_item: NEWTYPE AS NEWTYPE
#line 458 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = PyString_FromString("NewType"); }
#line 1764 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 98: // alias_or_constant: NAME '=' type maybe_type_ignore
#line 462 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj)); }
#line 1770 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 99: // alias_or_constant: NAME '=' '[' maybe_string_list ']' maybe_type_ignore
#line 463 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                         { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[5].value.obj), (yystack_[2].value.obj)); }
#line 1776 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 100: // maybe_string_list: string_list maybe_comma
#line 467 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                            { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1782 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 101: // maybe_string_list: %empty
#line 468 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1788 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 102: // string_list: string_list ',' STRING
#line 472 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1794 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 103: // string_list: STRING
#line 473 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1800 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 104: // typevardef: NAME '=' TYPEVAR '(' STRING typevar_args ')'
#line 477 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                 {
      (yylhs.value.obj) = ctx->Call(kAddTypeVar, "(NNN)", (yystack_[6].value.obj), (yystack_[2].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1809 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 105: // typevar_args: %empty
#line 484 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = Py_BuildValue("(OO)", Py_None, Py_None); }
#line 1815 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 106: // typevar_args: ',' type_list
#line 485 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NO)", (yystack_[0].value.obj), Py_None); }
#line 1821 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 107: // typevar_args: ',' typevar_kwargs
#line 486 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = Py_BuildValue("(ON)", Py_None, (yystack_[0].value.obj)); }
#line 1827 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 108: // typevar_args: ',' type_list ',' typevar_kwargs
#line 487 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                     { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1833 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 109: // typevar_kwargs: typevar_kwargs ',' typevar_kwarg
#line 491 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                     { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1839 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 110: // typevar_kwargs: typevar_kwarg
#line 492 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1845 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 111: // typevar_kwarg: NAME '=' type
#line 496 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1851 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 112: // typevar_kwarg: NAME '=' STRING
#line 498 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1857 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 113: // funcdef: decorators maybe_async DEF funcname '(' maybe_type_ignore params ')' return maybe_body
#line 503 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               {
      (yylhs.value.obj) = ctx->Call(kNewFunction, "(NONNNN)", (yystack_[9].value.obj), (yystack_[8].value.obj), (yystack_[6].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj));
      // Decorators is nullable and messes up the location tracking by
      // using the previous symbol as the start location for this production,
      // which is very misleading.  It is better to ignore decorators and
      // pretend the production started with DEF.  Even when decorators are
      // present the error line will be close enough to be helpful.
      yylhs.location.begin = yystack_[7].location.begin;
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1872 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 114: // funcname: NAME
#line 516 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1878 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 115: // funcname: COLL_NAMEDTUPLE
#line 517 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { (yylhs.value.obj) = PyString_FromString("namedtuple"); }
#line 1884 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 116: // funcname: NEWTYPE
#line 518 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyString_FromString("NewType"); }
#line 1890 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 117: // funcname: TYPEDDICT
#line 519 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              { (yylhs.value.obj) = PyString_FromString("TypedDict"); }
#line 1896 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 118: // decorators: decorators decorator
#line 523 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                         { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1902 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 119: // decorators: %empty
#line 524 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1908 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 120: // decorator: '@' dotted_name maybe_type_ignore
#line 528 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                      { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1914 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 121: // maybe_async: ASYNC
#line 532 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
          { (yylhs.value.obj) = Py_True; }
#line 1920 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 122: // maybe_async: %empty
#line 533 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = Py_False; }
#line 1926 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 123: // params: param_list maybe_comma
#line 537 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1932 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 124: // params: %empty
#line 538 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1938 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 125: // param_list: param_list ',' maybe_type_ignore param
#line 550 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                           { (yylhs.value.obj) = AppendList((yystack_[3].value.obj), (yystack_[0].value.obj)); }
#line 1944 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 126: // param_list: param
#line 551 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
          { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1950 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 127: // param: NAME param_type param_default
#line 555 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                  { (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[2].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1956 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 128: // param: '*'
#line 556 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.obj) = Py_BuildValue("(sOO)", "*", Py_None, Py_None); }
#line 1962 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 129: // param: param_star_name param_type
#line 557 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                               { (yylhs.value.obj) = Py_BuildValue("(NNO)", (yystack_[1].value.obj), (yystack_[0].value.obj), Py_None); }
#line 1968 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 130: // param: ELLIPSIS
#line 558 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1974 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 131: // param_type: ':' type
#line 562 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1980 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 132: // param_type: %empty
#line 563 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1986 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 133: // param_default: '=' NAME
#line 567 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1992 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 134: // param_default: '=' NUMBER
#line 568 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1998 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 135: // param_default: '=' ELLIPSIS
#line 569 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 2004 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 136: // param_default: %empty
#line 570 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 2010 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 137: // param_star_name: '*' NAME
#line 574 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = PyString_FromFormat("*%s", PyString_AsString((yystack_[0].value.obj))); }
#line 2016 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 138: // param_star_name: '*' '*' NAME
#line 575 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = PyString_FromFormat("**%s", PyString_AsString((yystack_[0].value.obj))); }
#line 2022 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 139: // return: ARROW type
#line 579 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2028 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 140: // return: %empty
#line 580 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 2034 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 141: // typeignore: TYPECOMMENT NAME
#line 584 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { Py_DecRef((yystack_[0].value.obj)); }
#line 2040 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 142: // typeignore: TYPECOMMENT NAME '[' maybe_type_list ']'
#line 585 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                             {
      Py_DecRef((yystack_[3].value.obj));
      Py_DecRef((yystack_[1].value.obj));
    }
#line 2049 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 143: // maybe_body: ':' typeignore INDENT body DEDENT
#line 592 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                      { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2055 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 144: // maybe_body: ':' INDENT body DEDENT
#line 593 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2061 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 145: // maybe_body: empty_body
#line 594 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = PyList_New(0); }
#line 2067 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 153: // body: body body_stmt
#line 608 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                   { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 2073 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 154: // body: body_stmt
#line 609 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2079 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 155: // body_stmt: NAME '=' type
#line 613 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2085 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 156: // body_stmt: RAISE type
#line 614 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2091 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 157: // body_stmt: RAISE type '(' ')'
#line 615 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2097 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 158: // type_parameters: type_parameters ',' type_parameter
#line 619 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                       { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2103 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 159: // type_parameters: type_parameter
#line 620 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                   { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2109 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 160: // type_parameter: type
#line 624 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2115 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 161: // type_parameter: ELLIPSIS
#line 625 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 2121 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 162: // type_parameter: NUMBER
#line 627 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2127 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 163: // type_parameter: STRING
#line 628 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2133 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 164: // type_parameter: '[' maybe_type_list ']'
#line 630 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                            {
      (yylhs.value.obj) = ctx->Call(kNewType, "(sN)", "tuple", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2142 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 165: // maybe_type_list: type_list maybe_comma
#line 637 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                          { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2148 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 166: // maybe_type_list: %empty
#line 638 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 2154 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 167: // type_list: type_list ',' type
#line 642 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2160 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 168: // type_list: type
#line 643 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2166 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 169: // type: dotted_name
#line 647 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                {
      (yylhs.value.obj) = ctx->Call(kNewType, "(N)", (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2175 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 170: // type: dotted_name '[' '(' ')' ']'
#line 651 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                {
      (yylhs.value.obj) = ctx->Call(kNewType, "(NN)", (yystack_[4].value.obj), PyList_New(0));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2184 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 171: // type: dotted_name '[' type_parameters maybe_comma ']'
#line 655 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2193 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 172: // type: NAMEDTUPLE '(' STRING ',' named_tuple_fields maybe_comma ')'
#line 659 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                                 {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2202 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 173: // type: COLL_NAMEDTUPLE '(' STRING ',' coll_named_tuple_fields maybe_comma ')'
#line 663 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                                           {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2211 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 174: // type: NEWTYPE '(' STRING ',' type maybe_comma ')'
#line 667 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                {
      (yylhs.value.obj) = ctx->Call(kNewNewType, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2220 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 175: // type: TYPEDDICT '(' STRING ',' typed_dict_fields maybe_typed_dict_kwarg ')'
#line 671 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                                          {
      (yylhs.value.obj) = ctx->Call(kNewTypedDict, "(NNN)", (yystack_[4].value.obj), (yystack_[2].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2229 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 176: // type: '(' type ')'
#line 675 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2235 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 177: // type: type AND type
#line 676 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = ctx->Call(kNewIntersectionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2241 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 178: // type: type OR type
#line 677 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = ctx->Call(kNewUnionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2247 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 179: // type: '?'
#line 678 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 2253 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 180: // type: NOTHING
#line 679 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = ctx->Value(kNothing); }
#line 2259 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 181: // named_tuple_fields: '[' named_tuple_field_list maybe_comma ']'
#line 683 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                               { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2265 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 182: // named_tuple_fields: '[' ']'
#line 684 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyList_New(0); }
#line 2271 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 183: // named_tuple_field_list: named_tuple_field_list ',' named_tuple_field
#line 688 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                 { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2277 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 184: // named_tuple_field_list: named_tuple_field
#line 689 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2283 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 185: // named_tuple_field: '(' STRING ',' type maybe_comma ')'
#line 693 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                         { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj)); }
#line 2289 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 188: // coll_named_tuple_fields: '[' coll_named_tuple_field_list maybe_comma ']'
#line 702 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2295 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 189: // coll_named_tuple_fields: '[' ']'
#line 703 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyList_New(0); }
#line 2301 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 190: // coll_named_tuple_field_list: coll_named_tuple_field_list ',' coll_named_tuple_field
#line 707 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                           {
      (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj));
    }
#line 2309 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 191: // coll_named_tuple_field_list: coll_named_tuple_field
#line 710 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2315 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 192: // coll_named_tuple_field: STRING
#line 714 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[0].value.obj), ctx->Value(kAnything)); }
#line 2321 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 193: // typed_dict_fields: '{' typed_dict_field_dict maybe_comma '}'
#line 718 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                              { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2327 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 194: // typed_dict_fields: '{' '}'
#line 719 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyDict_New(); }
#line 2333 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 195: // typed_dict_field_dict: typed_dict_field_dict ',' typed_dict_field
#line 723 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                               {
      PyDict_Update((yystack_[2].value.obj), (yystack_[0].value.obj));
      (yylhs.value.obj) = (yystack_[2].value.obj);
      Py_DECREF((yystack_[0].value.obj));
    }
#line 2343 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 196: // typed_dict_field_dict: typed_dict_field
#line 728 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2349 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 197: // typed_dict_field: STRING ':' NAME
#line 732 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { (yylhs.value.obj) = Py_BuildValue("{N: N}", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2355 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 198: // maybe_typed_dict_kwarg: ',' NAME '=' type maybe_comma
#line 736 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj)); }
#line 2361 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 199: // maybe_typed_dict_kwarg: maybe_comma
#line 737 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = Py_None; }
#line 2367 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 200: // type_tuple_elements: type_tuple_elements ',' type
#line 744 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                 { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2373 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 201: // type_tuple_elements: type ',' type
#line 745 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2379 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 202: // type_tuple_literal: '(' type_tuple_elements maybe_comma ')'
#line 754 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                            {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2388 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 203: // type_tuple_literal: '(' type ',' ')'
#line 759 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2397 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 204: // type_tuple_literal: type ','
#line 765 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             {
      Py_DECREF((yystack_[1].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2406 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 205: // dotted_name: NAME
#line 772 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2412 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 206: // dotted_name: dotted_name '.' NAME
#line 773 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                         {
#if PY_MAJOR_VERSION >= 3
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), DOT_STRING);
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), (yystack_[0].value.obj));
      Py_DECREF((yystack_[0].value.obj));
#else
      PyString_Concat(&(yystack_[2].value.obj), DOT_STRING);
      PyString_ConcatAndDel(&(yystack_[2].value.obj), (yystack_[0].value.obj));
#endif
      (yylhs.value.obj) = (yystack_[2].value.obj);
    }
#line 2428 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 207: // getitem_key: NUMBER
#line 787 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2434 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 208: // getitem_key: maybe_number ':' maybe_number
#line 788 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                  {
      PyObject* slice = PySlice_New((yystack_[2].value.obj), (yystack_[0].value.obj), NULL);
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2444 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 209: // getitem_key: maybe_number ':' maybe_number ':' maybe_number
#line 793 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                   {
      PyObject* slice = PySlice_New((yystack_[4].value.obj), (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2454 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 210: // maybe_number: NUMBER
#line 801 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2460 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 211: // maybe_number: %empty
#line 802 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = NULL; }
#line 2466 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;


#line 2470 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"

            default:
              break;
            }
        }
#if YY_EXCEPTIONS
      catch (const syntax_error& yyexc)
        {
          YYCDEBUG << "Caught exception: " << yyexc.what() << '\n';
          error (yyexc);
          YYERROR;
        }
#endif // YY_EXCEPTIONS
      YY_SYMBOL_PRINT ("-> $$ =", yylhs);
      yypop_ (yylen);
      yylen = 0;

      // Shift the result of the reduction.
      yypush_ (YY_NULLPTR, YY_MOVE (yylhs));
    }
    goto yynewstate;


  /*--------------------------------------.
  | yyerrlab -- here on detecting error.  |
  `--------------------------------------*/
  yyerrlab:
    // If not already recovering from an error, report this error.
    if (!yyerrstatus_)
      {
        ++yynerrs_;
        context yyctx (*this, yyla);
        std::string msg = yysyntax_error_ (yyctx);
        error (yyla.location, YY_MOVE (msg));
      }


    yyerror_range[1].location = yyla.location;
    if (yyerrstatus_ == 3)
      {
        /* If just tried and failed to reuse lookahead token after an
           error, discard it.  */

        // Return failure if at end of input.
        if (yyla.kind () == symbol_kind::S_YYEOF)
          YYABORT;
        else if (!yyla.empty ())
          {
            yy_destroy_ ("Error: discarding", yyla);
            yyla.clear ();
          }
      }

    // Else will try to reuse lookahead token after shifting the error token.
    goto yyerrlab1;


  /*---------------------------------------------------.
  | yyerrorlab -- error raised explicitly by YYERROR.  |
  `---------------------------------------------------*/
  yyerrorlab:
    /* Pacify compilers when the user code never invokes YYERROR and
       the label yyerrorlab therefore never appears in user code.  */
    if (false)
      YYERROR;

    /* Do not reclaim the symbols of the rule whose action triggered
       this YYERROR.  */
    yypop_ (yylen);
    yylen = 0;
    YY_STACK_PRINT ();
    goto yyerrlab1;


  /*-------------------------------------------------------------.
  | yyerrlab1 -- common code for both syntax error and YYERROR.  |
  `-------------------------------------------------------------*/
  yyerrlab1:
    yyerrstatus_ = 3;   // Each real token shifted decrements this.
    // Pop stack until we find a state that shifts the error token.
    for (;;)
      {
        yyn = yypact_[+yystack_[0].state];
        if (!yy_pact_value_is_default_ (yyn))
          {
            yyn += symbol_kind::S_YYerror;
            if (0 <= yyn && yyn <= yylast_
                && yycheck_[yyn] == symbol_kind::S_YYerror)
              {
                yyn = yytable_[yyn];
                if (0 < yyn)
                  break;
              }
          }

        // Pop the current state because it cannot handle the error token.
        if (yystack_.size () == 1)
          YYABORT;

        yyerror_range[1].location = yystack_[0].location;
        yy_destroy_ ("Error: popping", yystack_[0]);
        yypop_ ();
        YY_STACK_PRINT ();
      }
    {
      stack_symbol_type error_token;

      yyerror_range[2].location = yyla.location;
      YYLLOC_DEFAULT (error_token.location, yyerror_range, 2);

      // Shift the error token.
      error_token.state = state_type (yyn);
      yypush_ ("Shifting", YY_MOVE (error_token));
    }
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


  /*-----------------------------------------------------.
  | yyreturn -- parsing is finished, return the result.  |
  `-----------------------------------------------------*/
  yyreturn:
    if (!yyla.empty ())
      yy_destroy_ ("Cleanup: discarding lookahead", yyla);

    /* Do not reclaim the symbols of the rule whose action triggered
       this YYABORT or YYACCEPT.  */
    yypop_ (yylen);
    YY_STACK_PRINT ();
    while (1 < yystack_.size ())
      {
        yy_destroy_ ("Cleanup: popping", yystack_[0]);
        yypop_ ();
      }

    return yyresult;
  }
#if YY_EXCEPTIONS
    catch (...)
      {
        YYCDEBUG << "Exception caught: cleaning lookahead and stack\n";
        // Do not try to display the values of the reclaimed symbols,
        // as their printers might throw an exception.
        if (!yyla.empty ())
          yy_destroy_ (YY_NULLPTR, yyla);

        while (1 < yystack_.size ())
          {
            yy_destroy_ (YY_NULLPTR, yystack_[0]);
            yypop_ ();
          }
        throw;
      }
#endif // YY_EXCEPTIONS
  }

  void
  parser::error (const syntax_error& yyexc)
  {
    error (yyexc.location, yyexc.what ());
  }

  /* Return YYSTR after stripping away unnecessary quotes and
     backslashes, so that it's suitable for yyerror.  The heuristic is
     that double-quoting is unnecessary unless the string contains an
     apostrophe, a comma, or backslash (other than backslash-backslash).
     YYSTR is taken from yytname.  */
  std::string
  parser::yytnamerr_ (const char *yystr)
  {
    if (*yystr == '"')
      {
        std::string yyr;
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
              yyr += *yyp;
              break;

            case '"':
              return yyr;
            }
      do_not_strip_quotes: ;
      }

    return yystr;
  }

  std::string
  parser::symbol_name (symbol_kind_type yysymbol)
  {
    return yytnamerr_ (yytname_[yysymbol]);
  }



  // parser::context.
  parser::context::context (const parser& yyparser, const symbol_type& yyla)
    : yyparser_ (yyparser)
    , yyla_ (yyla)
  {}

  int
  parser::context::expected_tokens (symbol_kind_type yyarg[], int yyargn) const
  {
    // Actual number of expected tokens
    int yycount = 0;

    int yyn = yypact_[+yyparser_.yystack_[0].state];
    if (!yy_pact_value_is_default_ (yyn))
      {
        /* Start YYX at -YYN if negative to avoid negative indexes in
           YYCHECK.  In other words, skip the first -YYN actions for
           this state because they are default actions.  */
        int yyxbegin = yyn < 0 ? -yyn : 0;
        // Stay within bounds of both yycheck and yytname.
        int yychecklim = yylast_ - yyn + 1;
        int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
        for (int yyx = yyxbegin; yyx < yyxend; ++yyx)
          if (yycheck_[yyx + yyn] == yyx && yyx != symbol_kind::S_YYerror
              && !yy_table_value_is_error_ (yytable_[yyx + yyn]))
            {
              if (!yyarg)
                ++yycount;
              else if (yycount == yyargn)
                return 0;
              else
                yyarg[yycount++] = YY_CAST (symbol_kind_type, yyx);
            }
      }

    if (yyarg && yycount == 0 && 0 < yyargn)
      yyarg[0] = symbol_kind::S_YYEMPTY;
    return yycount;
  }



  int
  parser::yy_syntax_error_arguments_ (const context& yyctx,
                                                 symbol_kind_type yyarg[], int yyargn) const
  {
    /* There are many possibilities here to consider:
       - If this state is a consistent state with a default action, then
         the only way this function was invoked is if the default action
         is an error action.  In that case, don't check for expected
         tokens because there are none.
       - The only way there can be no lookahead present (in yyla) is
         if this state is a consistent state with a default action.
         Thus, detecting the absence of a lookahead is sufficient to
         determine that there is no unexpected or expected token to
         report.  In that case, just report a simple "syntax error".
       - Don't assume there isn't a lookahead just because this state is
         a consistent state with a default action.  There might have
         been a previous inconsistent state, consistent state with a
         non-default action, or user semantic action that manipulated
         yyla.  (However, yyla is currently not documented for users.)
       - Of course, the expected token list depends on states to have
         correct lookahead information, and it depends on the parser not
         to perform extra reductions after fetching a lookahead from the
         scanner and before detecting a syntax error.  Thus, state merging
         (from LALR or IELR) and default reductions corrupt the expected
         token list.  However, the list is correct for canonical LR with
         one exception: it will still contain any token that will not be
         accepted due to an error action in a later state.
    */

    if (!yyctx.lookahead ().empty ())
      {
        if (yyarg)
          yyarg[0] = yyctx.token ();
        int yyn = yyctx.expected_tokens (yyarg ? yyarg + 1 : yyarg, yyargn - 1);
        return yyn + 1;
      }
    return 0;
  }

  // Generate an error message.
  std::string
  parser::yysyntax_error_ (const context& yyctx) const
  {
    // Its maximum.
    enum { YYARGS_MAX = 5 };
    // Arguments of yyformat.
    symbol_kind_type yyarg[YYARGS_MAX];
    int yycount = yy_syntax_error_arguments_ (yyctx, yyarg, YYARGS_MAX);

    char const* yyformat = YY_NULLPTR;
    switch (yycount)
      {
#define YYCASE_(N, S)                         \
        case N:                               \
          yyformat = S;                       \
        break
      default: // Avoid compiler warnings.
        YYCASE_ (0, YY_("syntax error"));
        YYCASE_ (1, YY_("syntax error, unexpected %s"));
        YYCASE_ (2, YY_("syntax error, unexpected %s, expecting %s"));
        YYCASE_ (3, YY_("syntax error, unexpected %s, expecting %s or %s"));
        YYCASE_ (4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
        YYCASE_ (5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
#undef YYCASE_
      }

    std::string yyres;
    // Argument number.
    std::ptrdiff_t yyi = 0;
    for (char const* yyp = yyformat; *yyp; ++yyp)
      if (yyp[0] == '%' && yyp[1] == 's' && yyi < yycount)
        {
          yyres += symbol_name (yyarg[yyi++]);
          ++yyp;
        }
      else
        yyres += *yyp;
    return yyres;
  }


  const short parser::yypact_ninf_ = -350;

  const short parser::yytable_ninf_ = -211;

  const short
  parser::yypact_[] =
  {
     -11,  -350,   157,   181,   415,   210,  -350,  -350,    65,    29,
     212,    41,   189,  -350,  -350,   279,   203,  -350,  -350,  -350,
    -350,  -350,    76,  -350,   305,    48,  -350,    29,   296,   426,
      93,  -350,    -2,    90,   227,   201,   305,  -350,    29,   216,
     218,   233,  -350,    17,   212,  -350,   239,  -350,   234,   236,
     255,   258,   305,  -350,   298,   110,  -350,  -350,   264,   284,
     305,   318,   360,  -350,   217,    29,    29,  -350,  -350,  -350,
    -350,   332,  -350,  -350,   331,    73,   337,   212,  -350,  -350,
     349,   141,    92,  -350,   141,   304,   296,   333,   344,  -350,
    -350,   326,   326,     2,   338,   361,   365,   388,   398,   249,
     305,   305,   379,  -350,   149,   404,   305,   198,   377,  -350,
     378,   384,  -350,  -350,  -350,   416,  -350,   397,   399,   407,
    -350,  -350,   440,  -350,   409,  -350,  -350,   433,  -350,  -350,
     442,  -350,  -350,   364,  -350,   417,   423,  -350,   141,    43,
     417,   431,  -350,  -350,  -350,   380,   185,   427,   429,  -350,
    -350,  -350,  -350,  -350,   439,   438,   441,   443,   445,  -350,
     454,  -350,   417,  -350,  -350,  -350,   246,   305,   446,  -350,
     302,   447,    20,   276,   305,   451,   417,   473,  -350,   444,
     475,   452,   305,   478,   460,   330,  -350,   364,   417,  -350,
     417,   395,   405,  -350,   450,   234,   258,  -350,   352,  -350,
     302,   417,   417,   417,   453,   455,   305,   448,  -350,   456,
     457,   461,   302,   197,   459,   327,   464,  -350,  -350,   302,
     302,  -350,  -350,  -350,    44,  -350,   467,    52,   462,  -350,
    -350,  -350,   356,  -350,  -350,  -350,  -350,  -350,   305,  -350,
     334,   432,   432,    18,   138,   466,    12,   466,   214,     9,
     468,  -350,  -350,   305,  -350,  -350,  -350,   469,   471,  -350,
     472,  -350,  -350,  -350,   475,   362,  -350,  -350,  -350,   302,
    -350,  -350,  -350,   419,  -350,   417,  -350,   470,  -350,    19,
     474,   476,  -350,   470,   487,  -350,   477,  -350,  -350,   479,
    -350,  -350,   480,  -350,   482,   483,   486,  -350,   484,  -350,
     490,  -350,   488,   302,   283,   492,   327,  -350,  -350,   504,
      99,   481,   180,  -350,  -350,   305,   485,  -350,   510,   498,
     158,  -350,  -350,   489,   493,   491,  -350,   513,   494,  -350,
    -350,   524,   526,   495,   497,  -350,  -350,   302,   469,  -350,
     471,   496,   499,  -350,   163,  -350,  -350,   279,   502,  -350,
    -350,  -350,   302,    22,  -350,  -350,   305,   503,    18,   305,
    -350,  -350,  -350,  -350,  -350,  -350,  -350,   305,  -350,  -350,
     237,   505,   506,   508,  -350,  -350,  -350,   302,   410,  -350,
    -350,  -350,   214,   214,   511,   512,  -350,   112,   434,   417,
     509,  -350,  -350,  -350,   223,   514,   305,   515,   115,  -350,
     516,   421,  -350,  -350,  -350,   269,   402,  -350,   305,   308,
    -350,  -350,  -350,  -350,   165,   517,  -350,  -350,   302,   518,
    -350,  -350,  -350
  };

  const unsigned char
  parser::yydefact_[] =
  {
      12,    12,     0,     0,   119,     0,     1,     2,     0,     0,
       0,     0,     0,     9,    11,    39,     0,     5,     7,     8,
      10,     6,   122,     3,     0,     0,   205,     0,    46,     0,
      14,    79,    80,     0,     0,    82,     0,    48,     0,     0,
       0,     0,   121,     0,     0,   118,     0,   180,     0,     0,
       0,     0,     0,   179,    14,   169,    65,    66,     0,    68,
       0,   101,    14,    67,     0,     0,     0,    63,    64,    61,
      62,   211,    59,    60,     0,     0,     0,     0,    74,    13,
       0,     0,     0,    83,     0,    14,    47,     0,     0,    12,
      17,    20,    20,    14,     0,     0,     0,     0,     0,     0,
       0,     0,     0,    70,     0,     0,     0,     0,   187,   103,
       0,   187,   204,    98,    55,    54,    53,   207,     0,     0,
     206,    49,     0,    50,   141,    78,    81,    89,    90,    91,
      92,    93,    94,     0,    95,    14,    84,    88,     0,     0,
      14,     0,    72,    12,    12,   119,     0,     0,     0,   120,
     114,   115,   116,   117,     0,     0,     0,     0,     0,   176,
     178,   177,    14,   162,   163,   161,     0,   166,   187,   159,
     160,   105,    14,     0,   186,     0,    14,   186,   100,     0,
     211,     0,   166,     0,     0,     0,    76,     0,    14,    75,
      14,   119,   119,    40,   205,    25,    26,    19,     0,    22,
      23,    14,    14,    14,     0,     0,     0,     0,    71,     0,
       0,   187,   168,   186,     0,     0,     0,    69,   203,   201,
     200,   202,    99,   102,     0,   210,   208,     0,     0,    96,
      97,    85,     0,    87,    77,    73,    41,    38,     0,    18,
       0,     0,     0,   124,     0,   187,     0,   187,   187,     0,
     187,   170,   164,   186,   165,   158,   171,   205,   107,   110,
     106,   104,    51,    52,   211,     0,    56,   142,    86,    24,
      21,   212,   213,    37,    16,    14,    15,   132,   130,   128,
       0,   187,   126,   132,     0,   182,   187,   184,   186,     0,
     192,   189,   187,   191,     0,     0,     0,   194,   187,   196,
     186,   199,     0,   167,     0,     0,     0,   209,    57,     0,
      37,     0,   119,    30,    27,     0,   136,   137,     0,   140,
      14,   123,   129,     0,   186,     0,   172,   186,     0,   173,
     174,     0,   186,     0,     0,   175,   112,   111,     0,   109,
     108,     0,     0,    28,     0,    36,    35,    43,     0,    32,
      33,    34,   131,     0,   127,   138,     0,   152,     0,     0,
     183,   181,   190,   188,   197,   195,   193,     0,    58,    29,
       0,     0,     0,     0,   133,   134,   135,   139,     0,   113,
     145,   125,   187,   187,     0,     0,    37,     0,     0,   146,
       0,   198,    37,    37,   119,     0,     0,     0,     0,   154,
       0,     0,   148,   147,   185,   119,   119,    44,     0,   156,
     151,   144,   153,   150,     0,     0,    45,    42,   155,     0,
     143,   149,   157
  };

  const short
  parser::yypgoto_[] =
  {
    -350,  -350,   528,   -86,   -43,  -307,  -350,   463,  -350,   295,
     309,   242,  -142,  -350,  -350,  -350,  -350,  -303,   199,   206,
     129,   335,   381,  -294,  -350,  -350,   500,   546,   -71,   425,
    -172,  -285,  -350,  -350,  -350,  -350,   256,   259,  -281,  -350,
    -350,  -350,  -350,  -350,  -350,   205,   278,  -350,  -350,  -350,
    -349,  -350,  -350,   164,  -237,  -350,   353,   385,   354,   -24,
    -350,  -350,   244,  -107,  -350,  -350,   243,  -350,  -350,   240,
    -350,  -350,  -350,    -3,  -350,  -170,  -271
  };

  const short
  parser::yydefgoto_[] =
  {
       0,     2,     3,     4,    78,    13,    92,   147,   198,   199,
     274,   311,   312,    14,    15,   346,   347,    16,    39,    40,
      28,   123,    75,    17,    18,    30,    31,    83,   135,   136,
     137,    19,   110,   111,    20,   216,   258,   259,    21,   154,
      22,    45,    46,   280,   281,   282,   316,   354,   283,   357,
      79,   379,   380,   398,   399,   168,   169,   210,   211,   212,
     245,   286,   287,   175,   247,   292,   293,   250,   298,   299,
     302,   108,    63,    55,   118,   119,   275
  };

  const short
  parser::yytable_[] =
  {
      54,    62,   313,   145,   178,   345,    29,    32,    35,   348,
     226,   103,    85,   140,   296,   233,    80,   290,   349,   113,
      90,   277,   317,     1,    29,   374,   375,   350,    99,   388,
      35,   351,    26,   100,   101,    29,   107,    76,    91,   313,
     403,    93,   142,    74,    26,   278,    26,    74,   262,   376,
     149,    26,    56,    57,   291,    76,   265,   191,   192,   297,
     233,   214,    29,    29,   279,   318,    27,   188,    47,    48,
      49,    50,    51,    58,    32,    59,   160,   161,   121,    35,
     170,   122,   172,    42,    43,    60,    33,   345,   139,    61,
     266,   348,   186,    26,   307,    26,    53,   189,   345,   345,
     349,    24,   348,   348,   254,    25,    81,   389,   138,   350,
     122,   349,   349,   351,   271,   395,   400,   402,   395,   208,
     350,   350,   200,    44,   351,   351,   272,   271,    76,   217,
     415,   396,    77,   222,   396,    82,    35,   139,   289,   272,
     294,   295,    99,   301,   127,   234,   397,   235,   411,   219,
     220,   104,    26,   163,   164,    74,    64,     6,   241,   242,
     243,   412,   128,   129,   130,   131,   132,    86,   395,    47,
      48,    49,    50,    51,   321,   284,   165,   412,   133,   325,
     285,     7,   248,   344,   396,   328,   166,   134,   194,   170,
     167,   333,     9,    76,   115,   116,  -186,    53,   420,    24,
      26,   163,   164,   370,    12,    47,   195,    49,    50,   196,
      23,   100,   101,   -31,   269,    26,   200,    47,    48,    49,
      50,    51,    52,   197,   165,    36,   344,   100,   101,   303,
      65,    66,   314,    53,    52,     9,   159,   173,   167,    41,
      26,    56,    57,    84,   394,    53,    74,    12,    94,    26,
     405,   406,    87,   288,    88,   114,   407,    47,    48,    49,
      50,    51,   100,   101,    59,    89,    47,    48,    49,    50,
      51,    95,   344,    96,    60,   390,   391,   358,    61,    26,
     337,     9,   303,    52,   209,    53,    26,   159,   336,    37,
      38,   352,    97,    12,    53,    98,    47,    48,    49,    50,
      51,   105,   416,    47,    48,    49,    50,    51,    26,    65,
      66,   100,   101,    52,   218,   100,   101,   100,   101,   106,
      52,   100,   101,   109,    53,    47,    48,    49,    50,    51,
     257,    53,   377,    76,   120,   382,   117,   194,   102,    76,
     124,   150,    52,   383,   141,   419,    62,    47,    48,    49,
      50,    51,   126,    53,    47,   195,    49,    50,   196,   127,
     151,   152,   153,   146,    52,   143,   155,   127,   231,   232,
     156,    52,   409,   100,   101,    53,   144,   128,   129,   130,
     131,   132,    53,     8,   418,   128,   129,   130,   131,   132,
     239,   240,     9,   157,   268,    76,    10,    11,     8,   112,
     308,   309,   134,   158,    12,   344,   162,     9,     8,   171,
     134,    10,    11,   193,     9,    -4,   174,     9,     8,    12,
     176,    10,    11,   177,   395,   271,    12,     9,   236,    12,
      66,    10,    11,  -210,   271,   417,   271,   272,   237,    12,
     396,   179,   387,   180,   181,    76,   272,   271,   272,   271,
     182,   183,    76,   310,    67,    68,    69,    70,   190,   272,
     184,   272,   187,   201,   273,   202,   401,    71,   101,    72,
      73,    74,    67,    68,    69,    70,   203,   204,   223,   225,
     205,   229,   206,   230,   207,   213,   215,    72,    73,   221,
     238,   227,   323,   334,   244,   338,   246,   249,   251,   252,
     253,   256,   261,   264,   267,   288,   315,   300,   341,   304,
     305,   306,   319,   355,   343,   320,   324,   326,   290,   327,
     329,   330,   331,   332,   356,   353,   335,   364,   359,     5,
     284,   296,   369,   361,   368,   270,   363,   367,   373,   378,
     386,   384,   385,   392,   393,   366,   371,   404,   410,   413,
     421,   276,   342,   372,   408,   148,   422,    34,   185,   263,
     224,   322,   340,   381,   339,   414,   255,   228,   360,   260,
     362,     0,   365,     0,     0,     0,     0,   125
  };

  const short
  parser::yycheck_[] =
  {
      24,    25,   273,    89,   111,   312,     9,    10,    11,   312,
     180,    54,    36,    84,     5,   187,    18,     5,   312,    62,
       3,     3,     3,    34,    27,     3,     4,   312,    52,   378,
      33,   312,     3,    13,    14,    38,    60,    35,    21,   310,
     389,    44,    85,    45,     3,    27,     3,    45,     4,    27,
      93,     3,     4,     5,    42,    35,     4,   143,   144,    50,
     232,   168,    65,    66,    46,    46,    37,   138,    20,    21,
      22,    23,    24,    25,    77,    27,   100,   101,     5,    82,
     104,    37,   106,     7,     8,    37,    45,   394,    45,    41,
      38,   394,   135,     3,   264,     3,    48,   140,   405,   406,
     394,    36,   405,   406,   211,    40,    16,   378,    16,   394,
      37,   405,   406,   394,    15,     3,   387,   388,     3,   162,
     405,   406,   146,    47,   405,   406,    27,    15,    35,   172,
     401,    19,    39,   176,    19,    45,   139,    45,   245,    27,
     247,   248,   166,   250,     3,   188,    34,   190,    33,   173,
     174,    41,     3,     4,     5,    45,    27,     0,   201,   202,
     203,   398,    21,    22,    23,    24,    25,    38,     3,    20,
      21,    22,    23,    24,   281,    37,    27,   414,    37,   286,
      42,     0,   206,     3,    19,   292,    37,    46,     3,   213,
      41,   298,    12,    35,    65,    66,    38,    48,    33,    36,
       3,     4,     5,    40,    24,    20,    21,    22,    23,    24,
       0,    13,    14,    33,   238,     3,   240,    20,    21,    22,
      23,    24,    37,    38,    27,    36,     3,    13,    14,   253,
      13,    14,   275,    48,    37,    12,    38,    39,    41,    36,
       3,     4,     5,    16,   386,    48,    45,    24,     9,     3,
     392,   393,    36,    39,    36,    38,    33,    20,    21,    22,
      23,    24,    13,    14,    27,    32,    20,    21,    22,    23,
      24,    37,     3,    37,    37,   382,   383,   320,    41,     3,
     304,    12,   306,    37,    38,    48,     3,    38,     5,    10,
      11,   315,    37,    24,    48,    37,    20,    21,    22,    23,
      24,    37,    33,    20,    21,    22,    23,    24,     3,    13,
      14,    13,    14,    37,    38,    13,    14,    13,    14,    35,
      37,    13,    14,     5,    48,    20,    21,    22,    23,    24,
       3,    48,   356,    35,     3,   359,     4,     3,    40,    35,
       3,     3,    37,   367,    40,    37,   370,    20,    21,    22,
      23,    24,     3,    48,    20,    21,    22,    23,    24,     3,
      22,    23,    24,    37,    37,    32,     5,     3,    38,    39,
       5,    37,   396,    13,    14,    48,    32,    21,    22,    23,
      24,    25,    48,     3,   408,    21,    22,    23,    24,    25,
      38,    39,    12,     5,    38,    35,    16,    17,     3,    39,
      38,    39,    46,     5,    24,     3,    27,    12,     3,     5,
      46,    16,    17,    33,    12,     0,    39,    12,     3,    24,
      42,    16,    17,    39,     3,    15,    24,    12,    33,    24,
      14,    16,    17,    36,    15,    33,    15,    27,    33,    24,
      19,    42,    32,    36,     4,    35,    27,    15,    27,    15,
      41,    18,    35,    34,    28,    29,    30,    31,    27,    27,
      18,    27,    39,    36,    32,    36,    32,    41,    14,    43,
      44,    45,    28,    29,    30,    31,    37,    39,     5,     4,
      39,     3,    39,    23,    39,    39,    39,    43,    44,    38,
      40,    39,     5,     3,    41,     3,    41,    49,    42,    42,
      39,    42,    38,    36,    42,    39,    36,    39,     4,    40,
      39,    39,    38,     3,    33,    39,    39,    38,     5,    39,
      38,    38,    36,    39,    26,    40,    38,     3,    39,     1,
      37,     5,    33,    42,    38,   240,    42,    40,    36,    36,
      32,    36,    36,    32,    32,    50,   347,    38,    33,    33,
      33,   242,   310,   347,    40,    92,    38,    11,   133,   224,
     179,   283,   306,   358,   305,   401,   213,   182,   324,   215,
     327,    -1,   332,    -1,    -1,    -1,    -1,    77
  };

  const signed char
  parser::yystos_[] =
  {
       0,    34,    52,    53,    54,    53,     0,     0,     3,    12,
      16,    17,    24,    56,    64,    65,    68,    74,    75,    82,
      85,    89,    91,     0,    36,    40,     3,    37,    71,   124,
      76,    77,   124,    45,    78,   124,    36,    10,    11,    69,
      70,    36,     7,     8,    47,    92,    93,    20,    21,    22,
      23,    24,    37,    48,   110,   124,     4,     5,    25,    27,
      37,    41,   110,   123,    71,    13,    14,    28,    29,    30,
      31,    41,    43,    44,    45,    73,    35,    39,    55,   101,
      18,    16,    45,    78,    16,   110,    71,    36,    36,    32,
       3,    21,    57,   124,     9,    37,    37,    37,    37,   110,
      13,    14,    40,    55,    41,    37,    35,   110,   122,     5,
      83,    84,    39,    55,    38,    71,    71,     4,   125,   126,
       3,     5,    37,    72,     3,    77,     3,     3,    21,    22,
      23,    24,    25,    37,    46,    79,    80,    81,    16,    45,
      79,    40,    55,    32,    32,    54,    37,    58,    58,    55,
       3,    22,    23,    24,    90,     5,     5,     5,     5,    38,
     110,   110,    27,     4,     5,    27,    37,    41,   106,   107,
     110,     5,   110,    39,    39,   114,    42,    39,   114,    42,
      36,     4,    41,    18,    18,    80,    55,    39,    79,    55,
      27,    54,    54,    33,     3,    21,    24,    38,    59,    60,
     110,    36,    36,    37,    39,    39,    39,    39,    55,    38,
     108,   109,   110,    39,   114,    39,    86,    55,    38,   110,
     110,    38,    55,     5,    73,     4,   126,    39,   108,     3,
      23,    38,    39,    81,    55,    55,    33,    33,    40,    38,
      39,    55,    55,    55,    41,   111,    41,   115,   110,    49,
     118,    42,    42,    39,   114,   107,    42,     3,    87,    88,
     109,    38,     4,    72,    36,     4,    38,    42,    38,   110,
      60,    15,    27,    32,    61,   127,    61,     3,    27,    46,
      94,    95,    96,    99,    37,    42,   112,   113,    39,   114,
       5,    42,   116,   117,   114,   114,     5,    50,   119,   120,
      39,   114,   121,   110,    40,    39,    39,   126,    38,    39,
      34,    62,    63,   127,    55,    36,    97,     3,    46,    38,
      39,   114,    97,     5,    39,   114,    38,    39,   114,    38,
      38,    36,    39,   114,     3,    38,     5,   110,     3,    88,
      87,     4,    62,    33,     3,    56,    66,    67,    68,    74,
      82,    89,   110,    40,    98,     3,    26,   100,    55,    39,
     113,    42,   117,    42,     3,   120,    50,    40,    38,    33,
      40,    69,    70,    36,     3,     4,    27,   110,    36,   102,
     103,    96,   110,   110,    36,    36,    32,    32,   101,   127,
     114,   114,    32,    32,    63,     3,    19,    34,   104,   105,
     127,    32,   127,   101,    38,    63,    63,    33,    40,   110,
      33,    33,   105,    33,   104,   127,    33,    33,   110,    37,
      33,    33,    38
  };

  const signed char
  parser::yyr1_[] =
  {
       0,    51,    52,    52,    53,    54,    54,    54,    54,    54,
      54,    54,    54,    55,    55,    56,    56,    57,    58,    58,
      58,    59,    59,    60,    60,    60,    60,    61,    61,    61,
      62,    62,    63,    63,    63,    63,    63,    63,    64,    64,
      65,    65,    66,    66,    67,    67,    68,    69,    70,    71,
      71,    71,    71,    71,    71,    71,    72,    72,    72,    73,
      73,    73,    73,    73,    73,    74,    74,    74,    74,    74,
      74,    74,    74,    74,    75,    75,    75,    75,    76,    76,
      77,    77,    78,    78,    79,    79,    79,    80,    80,    81,
      81,    81,    81,    81,    81,    81,    81,    81,    82,    82,
      83,    83,    84,    84,    85,    86,    86,    86,    86,    87,
      87,    88,    88,    89,    90,    90,    90,    90,    91,    91,
      92,    93,    93,    94,    94,    95,    95,    96,    96,    96,
      96,    97,    97,    98,    98,    98,    98,    99,    99,   100,
     100,   101,   101,   102,   102,   102,   103,   103,   103,   103,
     103,   103,   103,   104,   104,   105,   105,   105,   106,   106,
     107,   107,   107,   107,   107,   108,   108,   109,   109,   110,
     110,   110,   110,   110,   110,   110,   110,   110,   110,   110,
     110,   111,   111,   112,   112,   113,   114,   114,   115,   115,
     116,   116,   117,   118,   118,   119,   119,   120,   121,   121,
     122,   122,   123,   123,   123,   124,   124,   125,   125,   125,
     126,   126,   127,   127
  };

  const signed char
  parser::yyr2_[] =
  {
       0,     2,     2,     3,     1,     2,     2,     2,     2,     2,
       2,     2,     0,     1,     0,     7,     7,     1,     3,     2,
       0,     3,     1,     1,     3,     1,     1,     2,     3,     4,
       1,     1,     2,     2,     2,     2,     2,     0,     6,     1,
       5,     6,     6,     1,     5,     6,     2,     2,     1,     3,
       3,     6,     6,     3,     3,     3,     4,     5,     7,     1,
       1,     1,     1,     1,     1,     3,     3,     3,     3,     6,
       4,     6,     4,     6,     3,     5,     5,     6,     3,     1,
       1,     3,     1,     2,     1,     3,     4,     3,     1,     1,
       1,     1,     1,     1,     1,     1,     3,     3,     4,     6,
       2,     0,     3,     1,     7,     0,     2,     2,     4,     3,
       1,     3,     3,    10,     1,     1,     1,     1,     2,     0,
       3,     1,     0,     2,     0,     4,     1,     3,     1,     2,
       1,     2,     0,     2,     2,     2,     0,     2,     3,     2,
       0,     2,     5,     5,     4,     1,     2,     3,     3,     5,
       4,     4,     0,     2,     1,     3,     2,     4,     3,     1,
       1,     1,     1,     1,     3,     2,     0,     3,     1,     1,
       5,     5,     7,     7,     7,     7,     3,     3,     3,     1,
       1,     4,     2,     3,     1,     6,     1,     0,     4,     2,
       3,     1,     1,     4,     2,     3,     1,     3,     5,     1,
       3,     3,     4,     4,     2,     1,     3,     1,     3,     5,
       1,     0,     1,     1
  };


#if PYTYPEDEBUG || 1
  // YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
  // First, the terminals, then, starting at \a YYNTOKENS, nonterminals.
  const char*
  const parser::yytname_[] =
  {
  "\"end of file\"", "error", "\"invalid token\"", "NAME", "NUMBER",
  "STRING", "LEXERROR", "ASYNC", "CLASS", "DEF", "ELSE", "ELIF", "IF",
  "OR", "AND", "PASS", "IMPORT", "FROM", "AS", "RAISE", "NOTHING",
  "NAMEDTUPLE", "COLL_NAMEDTUPLE", "NEWTYPE", "TYPEDDICT", "TYPEVAR",
  "ARROW", "ELLIPSIS", "EQ", "NE", "LE", "GE", "INDENT", "DEDENT",
  "TRIPLEQUOTED", "TYPECOMMENT", "':'", "'('", "')'", "','", "'='", "'['",
  "']'", "'<'", "'>'", "'.'", "'*'", "'@'", "'?'", "'{'", "'}'", "$accept",
  "start", "unit", "alldefs", "maybe_type_ignore", "classdef",
  "class_name", "parents", "parent_list", "parent", "maybe_class_funcs",
  "class_funcs", "funcdefs", "if_stmt", "if_and_elifs", "class_if_stmt",
  "class_if_and_elifs", "if_cond", "elif_cond", "else_cond", "condition",
  "version_tuple", "condition_op", "constantdef", "importdef",
  "import_items", "import_item", "import_name", "from_list", "from_items",
  "from_item", "alias_or_constant", "maybe_string_list", "string_list",
  "typevardef", "typevar_args", "typevar_kwargs", "typevar_kwarg",
  "funcdef", "funcname", "decorators", "decorator", "maybe_async",
  "params", "param_list", "param", "param_type", "param_default",
  "param_star_name", "return", "typeignore", "maybe_body", "empty_body",
  "body", "body_stmt", "type_parameters", "type_parameter",
  "maybe_type_list", "type_list", "type", "named_tuple_fields",
  "named_tuple_field_list", "named_tuple_field", "maybe_comma",
  "coll_named_tuple_fields", "coll_named_tuple_field_list",
  "coll_named_tuple_field", "typed_dict_fields", "typed_dict_field_dict",
  "typed_dict_field", "maybe_typed_dict_kwarg", "type_tuple_elements",
  "type_tuple_literal", "dotted_name", "getitem_key", "maybe_number",
  "pass_or_ellipsis", YY_NULLPTR
  };
#endif


#if PYTYPEDEBUG
  const short
  parser::yyrline_[] =
  {
       0,   135,   135,   136,   140,   144,   145,   146,   147,   153,
     154,   155,   160,   164,   165,   172,   179,   189,   200,   201,
     202,   206,   207,   211,   212,   213,   214,   221,   222,   223,
     227,   228,   232,   233,   238,   239,   244,   245,   250,   253,
     258,   262,   275,   278,   283,   287,   299,   303,   307,   311,
     314,   317,   320,   323,   324,   325,   329,   330,   331,   337,
     338,   339,   340,   341,   342,   346,   350,   354,   358,   362,
     366,   370,   374,   378,   385,   389,   393,   399,   408,   409,
     413,   414,   419,   420,   427,   428,   429,   433,   434,   438,
     439,   442,   445,   448,   451,   454,   457,   458,   462,   463,
     467,   468,   472,   473,   477,   484,   485,   486,   487,   491,
     492,   496,   498,   502,   516,   517,   518,   519,   523,   524,
     528,   532,   533,   537,   538,   550,   551,   555,   556,   557,
     558,   562,   563,   567,   568,   569,   570,   574,   575,   579,
     580,   584,   585,   592,   593,   594,   598,   599,   600,   601,
     602,   603,   604,   608,   609,   613,   614,   615,   619,   620,
     624,   625,   627,   628,   630,   637,   638,   642,   643,   647,
     651,   655,   659,   663,   667,   671,   675,   676,   677,   678,
     679,   683,   684,   688,   689,   693,   697,   698,   702,   703,
     707,   710,   714,   718,   719,   723,   728,   732,   736,   737,
     744,   745,   754,   759,   765,   772,   773,   787,   788,   793,
     801,   802,   806,   807
  };

  void
  parser::yy_stack_print_ () const
  {
    *yycdebug_ << "Stack now";
    for (stack_type::const_iterator
           i = yystack_.begin (),
           i_end = yystack_.end ();
         i != i_end; ++i)
      *yycdebug_ << ' ' << int (i->state);
    *yycdebug_ << '\n';
  }

  void
  parser::yy_reduce_print_ (int yyrule) const
  {
    int yylno = yyrline_[yyrule];
    int yynrhs = yyr2_[yyrule];
    // Print the symbols being reduced, and their result.
    *yycdebug_ << "Reducing stack by rule " << yyrule - 1
               << " (line " << yylno << "):\n";
    // The symbols being reduced.
    for (int yyi = 0; yyi < yynrhs; yyi++)
      YY_SYMBOL_PRINT ("   $" << yyi + 1 << " =",
                       yystack_[(yynrhs) - (yyi + 1)]);
  }
#endif // PYTYPEDEBUG

  parser::symbol_kind_type
  parser::yytranslate_ (int t)
  {
    // YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to
    // TOKEN-NUM as returned by yylex.
    static
    const signed char
    translate_table[] =
    {
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
      37,    38,    46,     2,    39,     2,    45,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,    36,     2,
      43,    40,    44,    48,    47,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,    41,     2,    42,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,    49,     2,    50,     2,     2,     2,     2,
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
      35
    };
    // Last valid token kind.
    const int code_max = 290;

    if (t <= 0)
      return symbol_kind::S_YYEOF;
    else if (t <= code_max)
      return YY_CAST (symbol_kind_type, translate_table[t]);
    else
      return symbol_kind::S_YYUNDEF;
  }

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
} // pytype
#line 3318 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"

#line 810 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"


void pytype::parser::error(const location& loc, const std::string& msg) {
  ctx->SetErrorLocation(loc);
  pytype::Lexer* lexer = pytypeget_extra(scanner);
  if (lexer->error_message_) {
    PyErr_SetObject(ctx->Value(pytype::kParseError), lexer->error_message_);
  } else {
    PyErr_SetString(ctx->Value(pytype::kParseError), msg.c_str());
  }
}

namespace {

PyObject* StartList(PyObject* item) {
  return Py_BuildValue("[N]", item);
}

PyObject* AppendList(PyObject* list, PyObject* item) {
  PyList_Append(list, item);
  Py_DECREF(item);
  return list;
}

PyObject* ExtendList(PyObject* dst, PyObject* src) {
  // Add items from src to dst (both of which must be lists) and return src.
  // Borrows the reference to src.
  Py_ssize_t count = PyList_Size(src);
  for (Py_ssize_t i=0; i < count; ++i) {
    PyList_Append(dst, PyList_GetItem(src, i));
  }
  Py_DECREF(src);
  return dst;
}

}  // end namespace
