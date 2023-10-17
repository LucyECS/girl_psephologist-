# Import the required libraries
import xml.etree.ElementTree as ET
import csv

# The header of the CSV file
header = ['Ward', 'GRN Candidate', 'ALP Candidate', 'LNP Candidate', 'GRN Votes', 'ALP Votes', 'LNP Votes', 'IND Votes', 'Formal Votes', 'Informal Votes', 'Number of Candidates', 
          'GRN%', 'ALP%', 'LNP%', 'IND%', 'informal%', 'Winner', 'Winner Party',
          '1st Excluded', '1 Party Excluded', '1GRN', '1ALP', '1LNP', '1IND', '1Exhausted', '1Distrubuted', '1GRN%', '1ALP%', '1LNP%', '1IND%', '1exhausted%',
          '2nd Excluded', '2 Party Excluded', '2GRN', '2ALP', '2LNP', '2IND', '2Exhausted', '2Distrubuted', '2GRN%', '2ALP%', '2LNP%', '2IND%', '2exhausted%',
          '3rd Excluded', '3 Party Excluded', '3GRN', '3ALP', '3LNP', '3IND', '3Exhausted', '3Distrubuted', '3GRN%', '3ALP%', '3LNP%', '3IND%', '3exhausted%',
          'TPP1 Party', 'TPP1 Votes', 'TPP2 Party', 'TPP2 Votes', 'Win Margin', 'Win Margin %', 'WARD', 'Hover Text']

# Dictionary of ballot names and party codes
abreviations = {'The Greens': 'GRN', 'Australian Labor Party': 'ALP', 'LNP': 'LNP', None: 'IND', 'Animal Justice Party': 'AJP'}

# WARD NAMES
WARD_NAMES = ['BRACKEN RIDGE', 'CALAMVALE', 'CENTRAL', 'CHANDLER', 'COORPAROO', 'DEAGON', 'DOBOY', 'FOREST LAKE', 'HAMILTON', 'JAMBOREE', 'MCDOWALL', 
 'MACGREGOR', 'MOOROOKA', 'NORTHGATE', 'ENOGGERA', 'HOLLAND PARK', 'MARCHANT', 
 'MORNINGSIDE', 'PADDINGTON', 'PULLENVALE', 'RUNCORN', 'TENNYSON', 'THE GABBA', 'THE GAP', 'WALTER TAYLOR', 'WYNNUM-MANLY']

# Read the XML file
tree = ET.parse('publicResults.xml')
root = tree.getroot()
districts = root[2][8][1][0]

# Open the CSV file
with open('Council2020.csv', 'w', encoding='UTF8', newline='') as coucnil_results:
    writer = csv.writer(coucnil_results)

    # write the header
    writer.writerow(header)

    # write the data
    for ward in districts:
        # Set up variables
        ward_name = ''
        grn_candidate = ''
        alp_candidate = ''
        lnp_candidate = ''
        num_candidates = 0
        grn_votes = 0
        alp_votes = 0
        lnp_votes = 0
        idp_votes = 0
        formal_count = 0
        informal_count = 0
        grn_percent = 0
        alp_percent = 0
        lnp_percent = 0
        idp_percent = 0
        informal_percent = 0
        winner = ''
        winner_party = ''
        hover_text = ''

        # Get the ward name
        ward_name = ward.get('districtName')

        # Get the candidate names
        candidates = ward[2]
        num_candidates = len(candidates)
        for candidate in candidates:
            if candidate.get('partyCode') == 'The Greens':
                grn_candidate = candidate.get('ballotName')
            if candidate.get('partyCode') == 'Australian Labor Party':
                alp_candidate = candidate.get('ballotName')
            if candidate.get('partyCode') == ('LNP'):
                lnp_candidate = candidate.get('ballotName')

        # Get the winner
        winner = ward[0].get('ballotName')
        winner_number = ward[0].get('ballotOrderNumber')
        for candidate in candidates:
            if candidate.get('ballotOrderNumber') == winner_number:
                winner_party = abreviations[candidate.get('partyCode')]

        # Get the formal and informal vote counts 
        firpref = ward[5]
        formal_count = firpref.find('totalFormalVotes').find('count').text
        informal_count = firpref.find('totalInformalVotes').find('count').text

        # Get the vote counts for each candidate
        for candidate in firpref.find('primaryVoteResults').findall('candidate'):
            if candidate.get('ballotName') == grn_candidate:
                grn_votes = candidate.find('count').text
            if candidate.get('ballotName') == alp_candidate:
                alp_votes = candidate.find('count').text
            if candidate.get('ballotName') == lnp_candidate:
                lnp_votes = candidate.find('count').text
        idp_votes = int(formal_count) - int(grn_votes) - int(alp_votes) - int(lnp_votes)

        # Calculate the percentages of the votes
        grn_percent = round(int(grn_votes)/int(formal_count)*100, 2)
        alp_percent = round(int(alp_votes)/int(formal_count)*100, 2)
        lnp_percent = round(int(lnp_votes)/int(formal_count)*100, 2)
        idp_percent = round(int(idp_votes)/int(formal_count)*100, 2)
        informal_percent = round(int(informal_count)/(int(formal_count)+int(informal_count))*100, 2)

        # Set up the row
        row = [ward_name, grn_candidate, alp_candidate, lnp_candidate, grn_votes, alp_votes, lnp_votes, idp_votes, formal_count, informal_count, num_candidates]
        row.extend([grn_percent, alp_percent, lnp_percent, idp_percent, informal_percent, winner, winner_party])

        # Get the hover text
        hover_text = ''
        hover_text += '<br>'
        hover_text += '<br>'        
        hover_text += 'WARD INFO<br>'
        hover_text += 'Ward: ' + ward_name + '<br>'
        hover_text += 'Winner: ' + winner + ' (' + winner_party + ')<br>'
        hover_text += 'Number of Candidates: ' + str(num_candidates) + '<br>'
        hover_text += 'Formal Votes: ' + str(formal_count) + '<br>'
        hover_text += 'Informal: ' + str(informal_count) + ' (' + str(informal_percent) + '%)<br>'
        hover_text += '------------------------<br>'
        hover_text += 'PRIMARY VOTES <br>'
        hover_text += 'GRN: ' + str(grn_votes) + ' (' + str(grn_percent) + '%)<br>'
        hover_text += 'ALP: ' + str(alp_votes) + ' (' + str(alp_percent) + '%)<br>'
        hover_text += 'LNP: ' + str(lnp_votes) + ' (' + str(lnp_percent) + '%)<br>'
        hover_text += 'IND: ' + str(idp_votes) + ' (' + str(idp_percent) + '%)<br>'

        # Get the preference flows
        prefflow = ward[6]
        for i in range(num_candidates-2):
            distribution = prefflow.find('preferenceDistributionSummary').findall('preferenceDistribution')[i]
            # Set up variables
            candidate_excluded = ''
            party_excluded = ''
            grn_flow = 0
            alp_flow = 0
            lnp_flow = 0
            idp_flow = 0
            exhausted = 0
            distributed = 0

            # Get the excluded candidate
            candidate_excluded = distribution.get('excludedBallotName')
            for candidate in candidates:
                if candidate.get('ballotName') == candidate_excluded:
                    party_excluded = abreviations[candidate.get('partyCode')]

            # Get the flow of votes for each candidate
            for candidate in distribution.findall('candidatePreferences'):
                if candidate.get('ballotName') == grn_candidate:
                    grn_flow = candidate.find('count').text
                if candidate.get('ballotName') == alp_candidate:
                    alp_flow = candidate.find('count').text
                if candidate.get('ballotName') == lnp_candidate:
                    lnp_flow = candidate.find('count').text

            # Get exhausted votes and distributed votes
            exhausted = distribution.find('exhausted').find('count').text
            distributed = distribution.find('votesDistributed').text

            # Calculate the flow of votes for the independent
            idp_flow = int(distributed) - int(grn_flow) - int(alp_flow) - int(lnp_flow)

            # Write the row
            row.extend([candidate_excluded, party_excluded, grn_flow, alp_flow, lnp_flow, idp_flow, exhausted])

            # Calculate the percentages
            grn_percent = round(int(grn_flow)/int(distributed)*100, 2)
            alp_percent = round(int(alp_flow)/int(distributed)*100, 2)
            lnp_percent = round(int(lnp_flow)/int(distributed)*100, 2)
            idp_percent = round(int(idp_flow)/int(distributed)*100, 2)
            exhausted_percent = round(int(exhausted)/(int(distributed)+int(exhausted))*100, 2)

            # Write the row
            row.extend([distributed, grn_percent, alp_percent, lnp_percent, idp_percent, exhausted_percent])

            # Add to the hover text
            hover_text += '------------------------<br>'
            hover_text += 'PREFERENCE FLOW ' + str(i+1) + '<br>'
            hover_text += 'Excluded: ' + candidate_excluded + ' (' + party_excluded + ')<br>'
            hover_text += 'Distributed: ' + str(distributed) + '<br>'
            hover_text += 'Exhausted: ' + str(exhausted) + ' (' + str(exhausted_percent) + '%)<br>'
            hover_text += 'GRN: ' + str(grn_flow) + ' (' + str(grn_percent) + '%)<br>'
            hover_text += 'ALP: ' + str(alp_flow) + ' (' + str(alp_percent) + '%)<br>'
            hover_text += 'LNP: ' + str(lnp_flow) + ' (' + str(lnp_percent) + '%)<br>'
            hover_text += 'IND: ' + str(idp_flow) + ' (' + str(idp_percent) + '%)<br>'

        # Add empty cells if there are less than 3 preference flows
        row.extend(['']*(57-len(row)))

        # Get the two party preferred
        # Set up variables
        tpp1_party = ''
        tpp1_votes = 0
        tpp2_party = ''
        tpp2_votes = 0
        tpp_candidate1 = ''
        tpp_candidate2 = ''

        # Get the two party preferred votes
        if num_candidates > 2:
            tpp = prefflow.find('twoCandidateVotes')
            tpp_candidate1 = tpp[0].get('ballotName')
            tpp_candidate2 = tpp[1].get('ballotName')
            for candidate in candidates:
                if candidate.get('ballotName') == tpp_candidate1:
                    tpp1_party = abreviations[candidate.get('partyCode')]
                if candidate.get('ballotName') == tpp_candidate2:
                    tpp2_party = abreviations[candidate.get('partyCode')]
            tpp1_votes = tpp[0].find('count').text
            tpp2_votes = tpp[1].find('count').text

        else:
            tpp1_party = abreviations[candidates[0].get('partyCode')]
            tpp1_votes = firpref.find('primaryVoteResults').findall('candidate')[0].find('count').text
            tpp2_party = abreviations[candidates[1].get('partyCode')]
            tpp2_votes = firpref.find('primaryVoteResults').findall('candidate')[1].find('count').text

        # Calculate the percentages
        tpp1_percent = round(int(tpp1_votes)/(int(tpp1_votes)+int(tpp2_votes))*100, 2)
        tpp2_percent = round(int(tpp2_votes)/(int(tpp1_votes)+int(tpp2_votes))*100, 2)

        # Win margin
        win_margin_votes = abs(int(tpp1_votes) - int(tpp2_votes))/2
        win_margin_percent = round(win_margin_votes/(int(tpp1_votes)+int(tpp2_votes))*100, 2)

        # Write the row
        row.extend([tpp1_party, tpp1_votes, tpp2_party, tpp2_votes, win_margin_votes, win_margin_percent])

        # Add to the hover text
        hover_text += '------------------------<br>'
        hover_text += 'TWO PARTY PREFERRED<br>'
        hover_text +=  tpp1_party + 'Votes: ' + str(tpp1_votes) + ' (' + str(tpp1_percent) + '%)<br>'
        hover_text +=  tpp2_party + 'Votes: ' + str(tpp2_votes) + ' (' + str(tpp2_percent) + '%)<br>'
        hover_text += 'Win Margin: ' + str(win_margin_votes) + ' (' + str(win_margin_percent) + '%)<br>'

        # Add the ward name and hover text
        row.append(WARD_NAMES.pop(0))
        row.append(hover_text)

        # Write the row
        writer.writerow(row)

