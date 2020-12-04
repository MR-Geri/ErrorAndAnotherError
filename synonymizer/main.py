import synonymizer.parse_model as parse
import synonymizer.chain as chain
from markovify import NewlineText


if __name__ == '__main__':
    with open('text.txt', encoding='utf-8') as file:
        # print(parse.generate_random_sentence(100, chain.make_markov_model(file.read().split())))
        # print(parse.generate_random_sentence(100, chain.make_higher_order_markov_model(5, file.read().split())))
        markov_model = NewlineText(file)
        [print(f'{markov_model.make_sentence()}\n') for _ in range(5)]
