### API Endpoint Documentation 

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/api/v1.0/questions'`

- Fetches a dictionary of questions in which keys are the question string, answer string, difficulty int, and category int at 10 per page.
- Request Args: page number - int
- Returns: An object with multiple keys, 'success': True, 'total_questions': totalQuestions, 'categories': categories 'questions': currentQuestions

```json
{
    "answer": "Apollo 13",
    "category": "5",
    "difficulty": "4",
    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
}
```

`POST '/api/v1.0/questions'`

- If there is a `{searchTerm}` present, will search for the term in the database, else posts a json object containing the key value pairs required to create a question (see above)
- Request Args: searchTerm - string, answer - string, questions - string, category - int, difficulty - int
- Returns: Either an object containing a success message and a dict of questions containing the search term, or creates a new question using json gathered from a form containing the question, answer, category, and difficulty.

```json
{
    "success": "True",
    "created": "new_question.id",
    "questions": "paginate_questions(request, selection)",
    "total_questions": "len(selection)"
}
```

`DELETE '/api/v1.0/questions/<int:id>'`

- Deletes a question using the provided Question.id
- Request Args: question id - int
- Returns: A json object containing a success message and the id of the deleted question

```json
{
    "success": "True",
    "deleted": "id",
    "message": "Question Deleted"
}
```

`GET '/categories/<int:id>/questions'`

- Gets a collection of questions within the provided category.id
- Request Args: category id - int
- Returns: An object containing a dict of questions in the specified category via the category id, the number of questions in said category, and the current category.

```json
{
    "success": "True",
    "questions": "pagedQ",
    "total_questions": "len(questions)",
    "current_category": "category.type"
}
```

`POST '/quizzes'`

- Posts a request for a new quiz question.
- Request Args: Quiz category - dict, previous questions - list
- Returns: An object containing a success message and a key:value pair containing the next random question formatted properly
```json
{
    "success": "True",
    "question": "nextQuestion.format()"
}
```

