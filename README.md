# Custom Compiler

## Overview
Custom Compiler is a project designed to parse and analyze a domain-specific language (DSL) using **lexical analysis** and **parsing techniques**. This compiler is built with **Python** and utilizes the `sly` library for defining the lexer and parser.

## Features
- **Lexical Analysis**: Tokenizes the source code into meaningful symbols.
- **Parsing**: Implements a recursive descent parser to check the syntax.
- **Symbol Table Management**: Stores variables, function definitions, and their attributes.
- **Semantic Analysis**: Detects type mismatches and undefined references.
- **Error Handling**: Provides clear error messages for syntax and semantic errors.

## Installation
To use the Custom Compiler, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sourabh-harapanahalli/Custom_Compiler.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd Custom_Compiler
   ```
3. **Install dependencies:**
   ```bash
   pip install sly
   ```

## Usage
To run the compiler on a DSL source file:
```bash
python Dlang_Compiler.py <source_file.dlang>
```

Example:
```bash
python Dlang_Compiler.py test-hw3.dlang
```

## Project Structure
```
Custom_Compiler/
│── Dlang_Compiler.py             # Main compiler script (lexer, parser, symbol table)
│── test-hw3.dlang                # Sample DSL program
│── README.md                     # Project documentation
│── auto_git_push.sh              # Script to automate Git commits and pushes
```

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

