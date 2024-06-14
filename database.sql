-- Execute all queries in DB to set up structure

-- USER is a reserved keyword with Postgres
-- You must use double quotes in every query that user is in:
-- ex. SELECT * FROM "user";
-- Otherwise you will have errors!

CREATE TABLE "user"(
    "id" SERIAL PRIMARY KEY,
    "username" VARCHAR(80) UNIQUE NOT NULL,
    "password" VARCHAR(1000) NOT NULL,
    "firstname" VARCHAR(80) NOT NULL,
    "lastname" VARCHAR(80) NOT NULL
);

CREATE TABLE "filetype"("id" SERIAL PRIMARY KEY);

CREATE TABLE "user_upload"(
    "id" SERIAL PRIMARY KEY,
    "user_id" BIGINT NOT NULL,
    "filetype" BIGINT NOT NULL,
    "name" VARCHAR(80) NOT NULL
);

CREATE TABLE "users_languages"(
    "id" SERIAL PRIMARY KEY,
    "user_id" BIGINT NOT NULL,
    "language_id" BIGINT NOT NULL,
    "skill" BIGINT NOT NULL DEFAULT '5'
);

CREATE TABLE "frameworks"(
    "id" SERIAL PRIMARY KEY,
    "name" BIGINT NOT NULL,
    "languages" BIGINT NOT NULL
);

CREATE TABLE "languages"(
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(80) NOT NULL
);

CREATE TABLE "users_frameworks"(
    "id" SERIAL PRIMARY KEY,
    "user_id" BIGINT NOT NULL,
    "framework_id" BIGINT NOT NULL,
    "skill" BIGINT NOT NULL DEFAULT '5'
);

-- CREATE TABLE "frameworks_list"(
--     "id" SERIAL PRIMARY KEY,
--     "react_native" BIGINT NOT NULL,
--     "nodejs" BIGINT NOT NULL,
--     "expressjs" BIGINT NOT NULL,
--     "jquery" BIGINT NOT NULL,
--     "django" BIGINT NOT NULL,
--     "flask" BIGINT NOT NULL,
--     "pytorch" BIGINT NOT NULL,
--     "git" BIGINT NOT NULL,
--     "ruby_on_rails" BIGINT NOT NULL,
--     "spring" BIGINT NOT NULL,
--     "spark" BIGINT NOT NULL,
--     "angularjs" BIGINT NOT NULL,
--     "reactjs" BIGINT NOT NULL,
--     "vuejs" BIGINT NOT NULL,
--     "pidgin" BIGINT NOT NULL,
--     "apache" BIGINT NOT NULL,
--     "tensorflow" BIGINT NOT NULL
-- );

-- CREATE TABLE "languages_list"(
--     "id" SERIAL PRIMARY KEY,
--     "python" BIGINT NOT NULL,
--     "javascript" BIGINT NOT NULL,
--     "sql" BIGINT NOT NULL,
--     "java" BIGINT NOT NULL,
--     "c" BIGINT NOT NULL,
--     "php" BIGINT NOT NULL,
--     "swift" BIGINT NOT NULL,
--     "css" BIGINT NOT NULL,
--     "html" BIGINT NOT NULL,
--     "go" BIGINT NOT NULL,
--     "kotlin" BIGINT NOT NULL,
--     "typescript" BIGINT NOT NULL,
--     "ruby" BIGINT NOT NULL,
--     "rust" BIGINT NOT NULL,
--     "c#" BIGINT NOT NULL
-- );

ALTER TABLE
    "frameworks" ADD CONSTRAINT "frameworks_languages_foreign" FOREIGN KEY("languages") REFERENCES "languages"("id");
ALTER TABLE
    "users_frameworks" ADD CONSTRAINT "users_frameworks_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "user"("id");
ALTER TABLE
    "users_frameworks" ADD CONSTRAINT "users_frameworks_framework_id_foreign" FOREIGN KEY("framework_id") REFERENCES "frameworks"("id");
ALTER TABLE
    "users_languages" ADD CONSTRAINT "users_languages_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "user"("id");
ALTER TABLE
    "user_upload" ADD CONSTRAINT "user_upload_filetype_foreign" FOREIGN KEY("filetype") REFERENCES "filetype"("id");
ALTER TABLE
    "users_languages" ADD CONSTRAINT "users_languages_language_id_foreign" FOREIGN KEY("language_id") REFERENCES "languages"("id");
ALTER TABLE
    "user_upload" ADD CONSTRAINT "user_upload_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "user"("id");


INSERT INTO api_vocab (word, definition) VALUES
('Algorithm', 'A step-by-step procedure for solving a problem or accomplishing some end, especially by a computer.'),
('API', 'Application Programming Interface; a set of functions and procedures that allow the creation of applications which access the features or data of an operating system, application, or other service.'),
('Array', 'An ordered series or arrangement of elements, typically of the same type.'),
('Bug', 'An error, flaw or fault in a computer program that causes it to produce an incorrect or unexpected result.'),
('Class', 'In object-oriented programming, a blueprint for creating objects, providing initial values for state and implementations of behavior.'),
('Compiler', 'A program that translates code written in high-level programming language into machine code that can be executed by a computer''s CPU.'),
('Database', 'An organized collection of data, generally stored and accessed electronically from a computer system.'),
('Debugging', 'The process of finding and fixing defects or problems within a computer program.'),
('Function', 'A block of organized, reusable code that performs a single action.'),
('Git', 'A distributed version-control system for tracking changes in source code during software development.'),
('IDE', 'Integrated Development Environment; a software suite that consolidates the basic tools developers need to write and test software.'),
('JSON', 'JavaScript Object Notation; a lightweight data-interchange format that is easy for humans to read and write, and easy for machines to parse and generate.'),
('Library', 'A collection of precompiled routines that a program can use, typically for performing common tasks.'),
('Loop', 'A sequence of instructions that repeats either a specified number of times or until a particular condition is met.'),
('Method', 'In object-oriented programming, a function that is associated with an object.'),
('Object', 'A collection of data (attributes) and methods that act on the data, representing an instance of a class in object-oriented programming.'),
('Open Source', 'Software for which the original source code is made freely available and may be redistributed and modified.'),
('Operator', 'A character or characters that represent an action or process, such as + for addition or == for comparison.'),
('Parameter', 'A variable used in a function or method to refer to one of the pieces of data provided as input to the function or method.'),
('Recursion', 'The process in which a function calls itself as a subroutine.'),
('Repository', 'A central place in which an aggregation of data is kept and maintained in an organized way, often used in the context of version control systems like Git.'),
('Runtime', 'The period of time when a program is running, starting when a program is executed and ending when the program terminates.'),
('Script', 'A set of commands in a file that can be executed without being compiled.'),
('SQL', 'Structured Query Language; a standardized programming language that is used to manage relational databases and perform various operations on the data in them.'),
('String', 'A sequence of characters, typically used to represent text.'),
('Syntax', 'The set of rules that defines the combinations of symbols that are considered to be correctly structured statements or expressions in a language.'),
('Variable', 'A storage location paired with an associated symbolic name, which contains some known or unknown quantity of information referred to as a value.'),
('Version Control', 'A system that records changes to a file or set of files over time so that you can recall specific versions later.'),
('Virtual Machine', 'An emulation of a computer system. Virtual machines are based on computer architectures and provide functionality of a physical computer.'),
('Framework', 'A platform for developing software applications, providing a foundation on which software developers can build programs for a specific platform.'),
('Inheritance', 'A feature of object-oriented programming where a class can inherit characteristics (methods and properties) from another class.'),
('Interface', 'A shared boundary across which two or more separate components of a computer system exchange information.'),
('Lambda', 'An anonymous function that can be defined within code, often used to encapsulate a small piece of functionality.'),
('Microservices', 'An architectural style that structures an application as a collection of loosely coupled services.'),
('Namespace', 'A container that holds a set of identifiers and allows the disambiguation of items with the same name.'),
('Polymorphism', 'A feature of object-oriented programming that allows one interface to be used for a general class of actions.'),
('Refactoring', 'The process of restructuring existing computer code without changing its external behavior.'),
('Software Development Life Cycle', 'A process for planning, creating, testing, and deploying an information system.'),
('Unit Test', 'A type of software testing where individual units or components of a software are tested.'),
('User Interface', 'The space where interactions between humans and machines occur.'),
('XML', 'eXtensible Markup Language; a markup language that defines a set of rules for encoding documents in a format that is both human-readable and machine-readable.'),
('YAML', 'YAML Ain''t Markup Language; a human-readable data serialization standard that can be used in conjunction with all programming languages.'),
('Agile', 'A set of principles for software development under which requirements and solutions evolve through the collaborative effort of self-organizing and cross-functional teams.'),
('Back-end', 'The part of a computer system or application that is not directly accessed by the user, typically responsible for storing and manipulating data.'),
('Front-end', 'The part of a computer system or application with which the user interacts directly.'),
('Middleware', 'Software that provides common services and capabilities to applications outside of what is offered by the operating system.'),
('ORM', 'Object-Relational Mapping; a programming technique for converting data between incompatible type systems using object-oriented programming languages.'),
('Singleton', 'A design pattern that restricts the instantiation of a class to one single instance.'),
('Thread', 'A sequence of programmed instructions that can be managed independently by a scheduler.'),
('Container', 'A lightweight, stand-alone, executable package of software that includes everything needed to run a piece of software, including the code, runtime, libraries, and settings.'),
('Continuous Integration', 'A practice in software engineering where code changes are automatically tested and merged to a shared repository frequently.')
;