# BERT  
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline

the_model = 'mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es'
tokenizer = AutoTokenizer.from_pretrained(the_model, do_lower_case=False)
model = AutoModelForQuestionAnswering.from_pretrained(the_model)


contexto = 'franquicia de medios que originalmente comenzó como un videojuego RPG, pero debido a su popularidad ha logrado expandirse a otros medios de entretenimiento como series de televisión, películas, juegos de cartas, ropa, entre otros, convirtiéndose en una marca que es reconocida en el mercado mundial. Las ventas de videojuegos hasta el 1 de diciembre de 2006 habían alcanzado una cantidad de 340 millones de ejemplares (incluyendo la venta de la versión Pikachu de la consola Nintendo 64),1​ logrando ocupar el segundo lugar de las sagas de videojuegos más vendidos de Nintendo.2​ La franquicia celebró su décimo aniversario el 27 de febrero de 2006.3​4​La saga de videojuegos es desarrollada por la compañía programadora de software japonesa Game Freak, con personajes creados por Satoshi Tajiri para la empresa de juguetes Creatures Inc., y a su vez distribuida por Nintendo. La misión en estos juegos es capturar y entrenar a los pokémon (criaturas cuya denominación da nombre al juego), que hasta la fecha alcanzan el número de 1025 (1172 incluyendo formas regionales y mecánicas exclusivas procedentes de otras entregas). La posibilidad de intercambiarlos le hizo conseguir una popularidad que se plasmó en un éxito de ventas y la consiguiente aparición de una serie animada, películas y diverso merchandising como peluches, juguetes y cartas.La producción de los videojuegos, serie de anime y demás material para su distribución en occidente fue realizada en Estados Unidos por 4Kids Entertainment hasta noviembre de 2005, momento en que decidió no renovar su contrato con Pokémon USA (una subsidiaria de Pokémon Company). Actualmente esta supervisa todo lo referente al material de Pokémon en su distribución en occidente.5​Actualmente la franquicia de pokémon ha alcanzado la cifra de 500 millones ejemplares lo largo de los años.'


nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)


def pregunta_respuesta(question : str): # model, contexto, nlp
  if not question:
    return {"error": "No question provided"}
    
  result = nlp({"question": question, "context": contexto})
  return {"question": question, "answer": result["answer"]}