import csv

# Define a dictionary to store dialogue-based conversation units
dialogues = {}

# Read the CSV file
with open('dialogueText.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    
    current_dialogue = None
    current_turn = 0 
    person_asking = None

    for row in csv_reader:
        folder, dialogueID, date, sender, receiver, text = row
        
        if dialogueID not in dialogues:
            dialogues[dialogueID] = {'questions': [], 'answers': []}
            person_asking = sender 
            person_answering = None
            current_turn = 0 
            current_dialogue = dialogueID 
        
        # Check if the current sender is the person asking 
        if sender == person_asking:
            if len(dialogues[dialogueID]['questions']) == 0:
                dialogues[dialogueID]['questions'].append(text)
            elif (len(dialogues[dialogueID]['questions']) >= current_turn + 1 and len(dialogues[dialogueID]['answers']) >= current_turn + 1):
                current_turn += 1 
                dialogues[dialogueID]['questions'].append(text)
            #Append to the previous question if no answer yet 
            else:
                dialogues[dialogueID]['questions'][current_turn] += ' ' + text
        else:
            # Append to the answer
            if len(dialogues[dialogueID]['answers']) == 0:
                person_answering = sender
                dialogues[dialogueID]['answers'].append(text)
            else:
                if person_answering != sender:
                    question = dialogues[dialogueID]['questions'][-1]
                    dialogues[dialogueID]['questions'].append(question)
                    dialogues[dialogueID]['answers'].append(text)
                    person_answering = sender
                else:
                    dialogues[dialogueID]['answers'][-1] += ' ' + text

        

output_file = 'dialogue_pairs.csv'

# Write the dialogue pairs to a CSV file
with open(output_file, mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(['DialogueID', 'Question', 'Answer'])
    
    # Write the dialogue-based question-answer pairs
    for dialogueID, dialog_data in dialogues.items():
        for question, answer in zip(dialog_data['questions'], dialog_data['answers']):
            writer.writerow([dialogueID, question, answer])

print(f'Dialogue pairs saved to {output_file}')






