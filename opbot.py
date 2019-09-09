import argparse
import subprocess

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def load_information(userfile, hostfile):
    users = open(userfile, 'r').read().lower().split('\n')

    hosts = open(hostfile, 'r').read().lower().split('\n')

    return users, hosts

def score_strings(users, hosts, compromised, threshold):
    scores = {}
    
    for user in compromised:
        scores[user] = process.extract(user, hosts, limit=threshold)

    return scores

def create_environment(users, hosts):
    environment = {}
    for user in users:
        environment[user] = []

        for host in hosts:
            environment[user].append(f'dir \\\\{host}\c$')

    return environment
                
def process_output_from_env(output):
    if 'Directory of' in output:
        reward = 10
        
        return reward

    if 'Access Denied' or 'not found' in output:
        reward = -10

        return reward

def main(args):

    compromised_users = args.compromised_users.split(',')
    # Gather user/host information
    users, hosts  = load_information(args.users, args.hosts)

    # Initialize Q and create the envrionment
    env = create_environment(users, hosts)

    # Gather the scores for users to hosts
    scores = score_strings(users, hosts, compromised_users, 5)

    # Have the agent learn
    Q_table = {}
    for user in compromised_users:
        Q_table[user] = []
        for host in scores[user]:
            if host[1] > 0:
                command = f'dir \\\\{host[0]}\\c$'

                cmd_results = subprocess.getoutput(f'cmd.exe /c {command}') # script engine hook

                reward = process_output_from_env(cmd_results)

                if args.verbose:
                    print(f'''
                        State (user): {user}
                        Running {command}
                        Reward: {reward}
                    ''')

                Q_table[user].append((command, reward))

    print(Q_table)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rwinforcement learning + String metrics for finding network privs', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u', '--users', help='Hsers file', default='.\\users.txt')
    parser.add_argument('-c', '--hosts', help='Hosts file', default='.\\hosts.txt')
    parser.add_argument('-r', '--compromised_users', help='Compromised users', required=True)
    parser.add_argument('-t', '--threshold', help='Number of scores to return')
    parser.add_argument('-v', '--verbose', help='Print results of each update to Q table', action='store_true')
    parser.add_argument('-d', '--debug', help='Print results of each update to Q table', action='store_true')
    args = parser.parse_args()
    
    main(args)