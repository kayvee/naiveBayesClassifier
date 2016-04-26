import sys, math

def process_line(line):
    #take line, strip off characters, split by tab
    label, subject_line = line.strip().split('\t')

    #from subject_line, make bag of words
    bow = subject_line.split()

    return label, bow

def update_counts(label, bow, label_freq, spam_freq, ham_freq):
    # update label_freq
    label_freq[label] += 1

    # if spam, update spam_freq
    if label == '1':
        for word in bow:
            spam_freq[word] = spam_freq.get(word, 1.0) + 1

    # if ham, update ham_freq
    elif label == '0':
        for word in bow:
            ham_freq[word] = ham_freq.get(word, 1.0) + 1

    return label_freq, spam_freq, ham_freq

def argmax(bow, label_prob, spam_prob, ham_prob):
    sProb = math.log(label_prob["1"])
    hProb = math.log(label_prob["0"])
    for word in bow:
        if word in spam_prob.keys():
            sProb += math.log(spam_prob[word])
        else:
           sProb += math.log(spam_prob["<UNK>"])

        if word in ham_prob.keys():
            hProb += math.log(ham_prob[word])
        else:
           hProb += math.log(ham_prob["<UNK>"])

    if sProb > hProb:
        return 1
    else:
        return 0

# runs the below code only if this is the main program run
if __name__ == '__main__':
    train = open("spam_assassin.train", "r")
    test = open("spam_assassin.test", "r")

    label_freq = {"0" : 0.0, "1" : 0.0}
    spam_freq = {"<UNK>" : 1.0}
    ham_freq = {"<UNK>" : 1.0}

    for line in train:
        label, bow = process_line(line)
        label_freq, spam_freq, ham_freq = update_counts(label, bow, label_freq, spam_freq, ham_freq)

    lsum = sum(label_freq.values())
    label_prob = {  "0" : label_freq["0"] / lsum,
                    "1" : label_freq["1"] / lsum
                    }

    spam_prob = {}
    ssum = sum(spam_freq.values())
    for key, value in spam_freq.iteritems():
        spam_prob[key] = value / ssum

    ham_prob = {}
    hsum = sum(ham_freq.values())
    for key, value in ham_freq.iteritems():
        ham_prob[key] = value / hsum

    actualSpams = 0.0
    trueSpams = 0.0
    guessedSpams = 0.0
    for line in test:
        label, bow = process_line(line)
        if label == '1':
            actualSpams +=1
        result = argmax(bow, label_prob, spam_prob, ham_prob)

        if result == 1:
            guessedSpams += 1
            if label == '1':
                trueSpams += 1

    #print trueSpams, guessedSpams, actualSpams
    precision = trueSpams / guessedSpams
    recall = trueSpams / actualSpams
                                        #Goals
    print "Precision:", precision       #71%
    print "Recall:", recall             #93%
