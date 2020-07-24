from PyInquirer import style_from_dict, Token, prompt, Separator

def main_menu():
  style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
  })

  option1 = 'Enter a Book Name'
  option2 = 'Upload a file with Book Names'

  questions = [
                {
                  'type': 'list',
                  'message': '',
                  'name': 'option',
                  'choices':  [
                                Separator('How do you want to add your book/s to Goodread?'),
                                  {
                                    'name': option1
                                  },
                                  {
                                    'name': option2
                                  },
                              ],
                  'validate': lambda answer: 'You must choose at least one.' \
                      if len(answer) == 0 else True
                }
              ]
  answers = prompt(questions, style=style)
  return answers['option']