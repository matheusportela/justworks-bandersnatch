import logging
import os
import time

FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('main')
logger.setLevel(os.environ.get('LOG', 'INFO').upper())

def pprint(string=""):
  for c in string:
    print(c, end='', flush=True)
    time.sleep(0.005)
  print()


class GameState:
  def __init__(self):
    self.company_type = None


class GameNode:
  def __init__(self, state):
    self.state = state

  def contract(self):
    raise NotImplementedError

  def text(self):
    """Return:
      node text
    """
    raise NotImplementedError

  def options(self):
    """Return:
    [
      (option text, node class, state changes)
    ]
    """
    raise NotImplementedError


class StartNode(GameNode):
  def contract(self):
    pass

  def text(self):
    return """Justworks: Bandersnatch
A Matheus Portela's game




Disclaimer: The information provided on this game does not, and is not intended to, constitute legal or accounting advice; instead, all information, content, and materials available on this site are for entertainment purposes only.
"""

  def options(self):
    return [
      ("OK. Let's start", Node0, {}),
    ]

class Node0(GameNode):
  def contract(self):
    pass

  def text(self):
    return """Jan 1st, 2018.

Your current job sucks, your boss is a jerk and you can't stand it anymore. You finally decided it is time to open your own company.

What sort of company are you going to open?
"""

  def options(self):
    return [
      ('Software consultancy', Node1, {'company type': 'software consultancy'}),
      ('Law firm', Node1, {'company type': 'law firm'}),
    ]


class Node1(GameNode):
  def contract(self):
    assert self.state['company type'] != None

  def text(self):
    return f"""Jan 2nd, 2018.

You used all your savings to create your own business, a {self.state['company type']}. Congrats!

First big decision: do you want to be a lone wolf or are you a team player?
"""

  def options(self):
    return [
      ('Lone wolf', Node2, {'number of employees': 0}),
      ('Team player', Node3, {'number of employees': 1}),
    ]


class Node2(GameNode):
  def contract(self):
    assert self.state['number of employees'] == 0

  def text(self):
    return f"""Jan 10th, 2018.
Company balance: $0

It isn't easy to find good employees when your company is just starting. Better to keep it to yourself.
"""

  def options(self):
    return [
      ('Keep rolling', Node4, {'balance': 100.00}),
    ]


class Node3(GameNode):
  def contract(self):
    assert self.state['number of employees'] == 1

  def text(self):
    return f"""Jan 10th, 2018.
Company balance: $0

It isn't easy to grow a business alone.

You called your best friend and she accepted the offer. You just hired your first employee!
"""

  def options(self):
    return [
      ('Keep rolling', Node4, {'balance': 100.00}),
    ]


class Node4(GameNode):
  def contract(self):
    assert self.state['balance'] > 0

  def text(self):
    return f"""Feb 1st, 2018.
Company balance: ${self.state['balance']}
Company size: {self.state['number of employees']}

Your company made its first sale and generated $100 in revenue. Time to pay taxes!

What tax form will you submit?
"""

  def options(self):
    wrong_form_balance = self.state['balance'] - 50.00
    right_form_balance = self.state['balance'] - 5.00

    if self.state['number of employees'] == 0:
      return [
        ('Form 1040', Node5, {'balance': wrong_form_balance}),
        ('Form 1099', Node5, {'balance': wrong_form_balance}),
        ('Form 1120', Node6, {'balance': right_form_balance}),
        ('Form 1164', Node5, {'balance': wrong_form_balance}),
      ]
    else:
      return [
        ('Form 1040', Node6, {'balance': right_form_balance}),
        ('Form 1099', Node5, {'balance': wrong_form_balance}),
        ('Form 1120', Node5, {'balance': wrong_form_balance}),
        ('Form 1164', Node5, {'balance': wrong_form_balance}),
      ]


class Node5(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Feb 15th, 2018.
Company balance: ${self.state['balance']}
Company size: {self.state['number of employees']}

MESSAGE FROM IRS: WRONG FORM!!!! YOUR FINE IS 50% >:(
"""

  def options(self):
    return [
      ('Tax sucks', Node7, {})
    ]

class Node6(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Feb 15th, 2018.
Company balance: ${self.state['balance']}
Company size: {self.state['number of employees']}

Message from IRS: We received your form. Your tax is 5%.
"""

  def options(self):
    return [
      ('Tax sucks', Node7, {})
    ]

class Node7(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Mar 1st, 2018.
Company balance: ${self.state['balance'] + 5_500}
Company size: {self.state['number of employees'] + 2}

Your company is growing fast. You made $5,500 this month and hired 2 new employees!
"""

  def options(self):
    return [
      ('Nice!', Node8, {'number of employees': self.state['number of employees'] + 2, 'balance': self.state['balance'] + 5_500}),
    ]

class Node8(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Apr 1st, 2018.
Company balance: ${self.state['balance']}
Company size: {self.state['number of employees']}

It's hard to keep track of all this bookkeeping. Time to hire an accountant. Which one will you choose?
"""

  def options(self):
    return [
      ('DIY YOLO ($0 per year)', Node9, {'accountant': 'self', 'accountant_cost': 0.00}),
      ('Your cousin ($50 per year)', Node9, {'accountant': 'cousin', 'accountant_cost': 50.00, 'balance': self.state['balance'] - 50}),
      ('Your friend from high-school that became an accountant ($1,000 per year)', Node9, {'accountant': 'contractor', 'accountant_cost': 1_000.00, 'balance': self.state['balance'] - 1_000}),
      ('The accounting firm you saw on Forbes Magazine ($15,000 per year)', Node10, {'accountant': 'firm', 'accountant_cost': 15_000.00, 'balance': self.state['balance'] - 15_000}),
    ]

class Node9(GameNode):
  def contract(self):
    assert self.state['accountant'] != None
    assert self.state['accountant_cost'] != None

  def text(self):
    return f"""Apr 15th, 2018.
Company balance: ${self.state['balance']}
Company size: {self.state['number of employees']}

Did you remember to file those I-9 forms?
"""

  def options(self):
    return [
      ('What?', Node11, {}),
      ('Of course... not', Node11, {}),
    ]

class Node10(GameNode):
  def contract(self):
    assert self.state['accountant'] == 'firm'

  def text(self):
    return f"""May 1st, 2018.
Company balance: ${self.state['balance']}
Company size: {self.state['number of employees']}

Message from accountant firm: You should declare bankruptcy.

If you had used Justworks, you could have reduced your accounting costs with our automated platform.

Good luck next time.
"""

  def options(self):
    return []

class Node11(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Apr 20th, 2018.
Company balance: ${self.state['balance']}
Company size: {self.state['number of employees']}

Message from USCIS: WHERE ARE THE I-9 FORMS??

Pay $4,575 in fines.
Also, submit the forms.
"""

  def options(self):
    new_balance = self.state['balance'] - 4_575

    if new_balance < 0:
      return [
        ('How was I supposed to know that?', Node12, {'balance': new_balance}),
        ('There must be a better way...', Node12, {'balance': new_balance}),
      ]
    else:
      return [
        ('How was I supposed to know that?', Node13, {'balance': new_balance}),
        ('There must be a better way...', Node13, {'balance': new_balance}),
      ]

class Node12(GameNode):
  def contract(self):
    assert self.state['balance'] < 0

  def text(self):
    if self.state['accountant'] != 'self':
      return f"""May 1st, 2018.
Company balance: ${self.state['balance']}
Company size: {self.state['number of employees']}

You do the math and realize your company is broke.

Did you know that Justworks helps you dealing with I-9 forms?

Good luck next time.
"""
    else:
      return f"""May 1st, 2018.
Company balance: ${self.state['balance']}
Company size: {self.state['number of employees']}

Message from accountant: You are broke :(

Did you know that Justworks helps you dealing with I-9 forms?

Good luck next time.
"""

  def options(self):
    return []

class Node13(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""May 1st, 2018.
Company balance: ${self.state['balance'] + 7000}
Company size: {self.state['number of employees']}

Monthly revenue: $7,000!

Your friend told you that her company is using Justworks for payroll, HR, and benefits.

According to their website, they could have helped you with the recent I-9 problem.

What do you do?
"""

  def options(self):
    return [
      ("I can manage it myself. No need to use this platform.", Node15, {'platform': None, 'balance': self.state['balance'] + 7000}),
      ("Justworks sound awesome! I'm gonna use it!", Node14, {'platform': 'justworks', 'balance': self.state['balance'] + 10_000}),
    ]

class Node14(GameNode):
  def contract(self):
    assert 'platform' in self.state

  def text(self):
    return f"""May 10th, 2018.
Company balance: ${self.state['balance']}
Company size: {self.state['number of employees']}

You enroll into Justworks through their and the onboarding team is great!
"""

  def options(self):
    return [
      ("Sounds like it's gonna be a nice journey with Justworks", Node15, {}),
    ]

class Node15(GameNode):
  def contract(self):
    assert 'platform' in self.state

  def text(self):
    return f"""Jun 1st, 2018.
Company balance: ${self.state['balance'] + 10_000}
Company size: {self.state['number of employees']}

Monthly revenue: $10,000!

One of your employees live in New Jersey...
"""

  def options(self):
    if self.state['platform'] == 'justworks':
      return [
        ("Is it a problem?", Node16, {'balance': self.state['balance'] + 10_000})
      ]
    if self.state['accountant'] == 'contractor':
      return [
        ("Is it a problem?", Node17, {'balance': self.state['balance'] + 10_000})
      ]
    return [
      ("Is it a problem?", Node18, {'balance': self.state['balance'] + 10_000})
    ]

class Node16(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Jun 1st, 2018.
Company balance: ${self.state['balance']}
Company size: {self.state['number of employees']}

Not really. Justworks identified it and filled the correct forms to New Jersey state.
"""

  def options(self):
    return [
      ('Justworks <3', Node19, {}),
    ]

class Node17(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Jun 1st, 2018.
Company balance: ${self.state['balance']}
Company size: {self.state['number of employees']}

Not really. Your accountant helped you figure it out in time.
"""

  def options(self):
    return [
      ('That was close', Node19, {}),
    ]

class Node18(GameNode):
  def contract(self):
    pass

  def text(self):
    if self.state['accountant'] == 'self':
      return f"""Jun 1st, 2018.
Company balance: ${self.state['balance'] - 5_000}
Company size: {self.state['number of employees']}

You are not a trained accountant and didn't know different forms should have been filed to New Jersey state.

Now, you have to pay $5,000 in penalties.
"""
    else:
      return f"""Jun 1st, 2018.
Company balance: ${self.state['balance'] - 5_000}
Company size: {self.state['number of employees']}

You figure out your cousin isn't the best accountant in the world and didn't notice it either.

Now, you have to pay $5,000 in penalties.
"""

  def options(self):
    return [
      ("Oh no :(", Node19, {'balance': self.state['balance'] - 5_000}),
    ]

class Node19(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Jul 1st, 2018.
Company balance: ${self.state['balance'] + 15000}
Company size: {self.state['number of employees']}

Your company is growing fast. This month's revenue was $15,000!

However, your employees cannot handle everything by themselves. It's hiring season!
"""

  def options(self):
    if self.state['platform'] == 'justworks':
      return [
        ("Let's grow this company!", Node20, {'balance': self.state['balance'] + 15000}),
      ]
    else:
      return [
        ("Let's grow this company!", Node21, {'balance': self.state['balance'] + 15000}),
      ]

class Node20(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Jul 31st, 2018.
Company balance: ${self.state['balance']}
Company size: {self.state['number of employees'] + 15}

Thanks to all the benefits available through Justworks, you were able to hire 15 new employees!
"""

  def options(self):
    return [
      ("OMG. Justworks is the best.", Node22, {'number of employees': self.state['number of employees'] + 15})
    ]

class Node21(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Jul 31st, 2018.
Company balance: ${self.state['balance']}
Company size: {self.state['number of employees'] + 2}

It's hard to convince people to join your company when you don't offer health insurance, 401(k), and perks...

You could only hire 2 good friends that believe in you.
"""

  def options(self):
    return [
      ("I wish life was easier...", Node22, {'number of employees': self.state['number of employees'] + 2})
    ]

class Node22(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Aug 1st, 2018.
Company balance: ${self.state['balance'] + 25000}
Company size: {self.state['number of employees']}

Relax, it's payday. Enjoy the extra $25,000 in your company bank account.
"""

  def options(self):
    return [
      ("\\o/", Node23, {'balance': self.state['balance'] + 25000})
    ]

class Node23(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Aug 15th, 2018.
Company balance: ${self.state['balance']}
Company size: {self.state['number of employees']}

Some of your employees want to have access to better medical, dental, and vision insurance. What do you want to do?
"""

  def options(self):
    if self.state['platform'] == 'justworks':
      return [
        ("Of course, everyone deserves good health care", Node24, {}),
        ("Can I afford it?", Node24, {}),
      ]
    else:
      return [
        ("I'll go on and hire a health insurance", Node25, {}),
        ("Sorry, they'll have to pay from their own pockets", Node26, {}),
      ]

class Node24(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Aug 15th, 2018.
Company balance: ${self.state['balance'] + 15000}
Company size: {self.state['number of employees'] + 2}

You can afford doing so because through Justworks, offering excellent health insurance options to your employees is way cheaper than doing it yourself.

Their enthusiasm results in extra $15,000 in sales this month and 2 more employees.
"""

  def options(self):
    return [
      ("Treating your employees well is a great business strategy", Node27, {'balance': self.state['balance'] + 15000, 'number of employees': self.state['number of employees'] + 2})
    ]

class Node25(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Aug 15th, 2018.
Company balance: ${self.state['balance'] - 40000}
Company size: {self.state['number of employees'] - 3}

The only health insurance policy available to your company costs $40,000 and isn't that great.

3 employees decide to leave your company because of poor benefits.
"""

  def options(self):
    return [
      ("I wish I could have better health insurance quotes...", Node27, {'balance': self.state['balance'] - 40000, 'number of employees': self.state['number of employees'] - 3})
    ]

class Node26(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Aug 15th, 2018.
Company balance: ${self.state['balance']}
Company size: {0}

All your employees decide to quit. You lose all your clients and your company cannot continue operating.

If you had used Justworks as your PEO, you would be able to offer excellent benefit offers to your employees while being affordable to your company.

Good luck next time.
"""

  def options(self):
    return [
    ]

class Node27(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Sep 1st, 2018.
Company balance: ${self.state['balance'] + 10000}
Company size: {self.state['number of employees']}

This month wasn't as good as the previous ones.

Maybe, hiring a contractor to build a new website will help you. What do you think?
"""

  def options(self):
    return [
      ("Let's do it ($20,000)", Node28, {'balance': self.state['balance'] + 10000 - 20000}),
      ("Nah", Node29, {'balance': self.state['balance'] + 10000}),
    ]

class Node28(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Oct 1st, 2018.
Company balance: ${self.state['balance'] + 70000}
Company size: {self.state['number of employees']}

The new website is driving a lot of new leads: $70,000 in revenue this month! Good choice.
"""

  def options(self):
    return [
      ("Yay", Node30, {'balance': self.state['balance'] + 70000}),
    ]

class Node29(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Oct 1st, 2018.
Company balance: ${self.state['balance'] - 15000}
Company size: {self.state['number of employees']}

This month was even tougher than the previous one. Your deficit is $15,000.
"""

  def options(self):
    return [
      ("Oh no", Node32, {'balance': self.state['balance'] - 15000}),
    ]

class Node30(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Oct 15th, 2018.
Company balance: ${self.state['balance']}
Company size: {self.state['number of employees']}

Do you know how to fill 1099 forms?
"""

  def options(self):
    if self.state['platform'] == 'justworks':
      return [
        ("No, but Justworks does it for me", Node32, {}),
      ]
    else:
      return [
        ("No...", Node31, {}),
      ]

class Node31(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Oct 25th, 2018.
Company balance: ${self.state['balance']}
Company size: {self.state['number of employees']}

IRS says: Yeah... I noticed. Your form was wrong and I'm gonna fine you in $15,000.
"""

  def options(self):
    return [
      ("I guess a PEO would be able to help me filling forms 1099...", Node32, {}),
    ]

class Node32(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Nov 1st, 2018.
Company balance: ${self.state['balance'] + 3000}
Company size: {self.state['number of employees']}

Brace yourself
Winter is coming
"""

  def options(self):
    return [
      ("RIP Ned Stark", Node33, {'balance': self.state['balance'] + 3000}),
    ]

class Node33(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Dec 1st, 2018.
Company balance: ${self.state['balance']}
Company size: {self.state['number of employees']}

EMERGENCY!!!

The largest snow storm in history (due to climate change, btw)

Banks are shut down

People cannot leave their houses

Horror

Panic
"""

  def options(self):
    if self.state['platform'] == 'justworks':
      return [
        ("HOW AM I GOING TO PAY MY EMPLOYEES??? WHAT SHOULD I DO??? CAN I CALL MY MOM???", Node34, {}),
      ]
    else:
      return [
        ("HOW AM I GOING TO PAY MY EMPLOYEES??? WHAT SHOULD I DO??? CAN I CALL MY MOM???", Node35, {}),
      ]

class Node34(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Dec 31st, 2018.
Company balance: ${self.state['balance']}
Company size: {self.state['number of employees']}

Justworks 24/7 customer support team is here to help you!

They instruct you in what should do to pay your employees.

It wasn't easy but they moved mountains to ensure your company was going to survive through this hardship.

You trust them and, together, you fix everything.
"""

  def options(self):
    return [
      ("JUSTWORKS THE BEST!", Node36, {}),
    ]

class Node35(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Dec 31st, 2018.
Company balance: ${0}
Company size: {0}

Unfortunately, you bank does not help you through this nightmare. After all, their customer support is shit.

No one is able to help you.

You are alone in this world.

Your employees sue you because they didn't receive their money in a timely manner.

There is not much you can do besides declaring bankruptcy.

Consider using Justworks next time. I've heard their customer support is the best in class.
"""

  def options(self):
    return []

class Node36(GameNode):
  def contract(self):
    pass

  def text(self):
    return f"""Jan 1st, 2021.
Company balance: ${100_000_000_000}
Company size: {100}

After surviving this nightmare, nothing is going to stop your company.

With Justworks' help, you are able to grow your small start-up to a multi-billion company in 3 years.

Your employees are happy. Their benefits are awesome. Their paycheck, even better. They are physically and mentally healthy.

The world is a better place.

Thanks for being a Justworks customer. We made it together.
"""

  def options(self):
    return []

class Engine:
  def __init__(self, initial_node_class=StartNode, initial_state={}):
    self.node = initial_node_class(state=initial_state)

  def run(self):
    while True:
      logger.debug(f'Game step')

      self.assert_node_contract()
      self.print_node_text()

      if self.is_game_over():
        break

      selected_option = self.select_node_option()
      self.node = self.transition_to_selected_node(selected_option)

  def assert_node_contract(self):
    self.node.contract()

  def print_node_text(self):
    # for _ in range(100):
    #   print()
    os.system('clear')
    pprint(self.node.text())

  def select_node_option(self):
    options = self.node.options()

    while True:
      for i, (text, _, _) in enumerate(options):
        pprint(f'{i+1}) {text}')

      try:
        selected_option = int(input('> '))
        if selected_option <= 0 or selected_option > len(options):
          raise AttributeError
      except ValueError:
        print(f'Option must be a number. Try again.')
      except AttributeError:
        if len(options) == 1:
          print(f'Option must be 1. Try again.')
        else:
          print(f'Option must be from 1 to {len(options)}. Try again.')
      except (KeyboardInterrupt, EOFError):
        exit(1)
      else:
        break

    return selected_option - 1

  def transition_to_selected_node(self, selected_option):
    (_, new_node_class, state_change) = self.node.options()[selected_option]
    new_state = {**self.node.state, **state_change}
    return new_node_class(new_state)

  def is_game_over(self):
    return self.node.options() == []


def main():
  engine = Engine()
  engine.run()


if __name__ == '__main__':
  main()
