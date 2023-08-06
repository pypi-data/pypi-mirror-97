import requests
import json
import logging



##slack.setup('name') should be called in the loop, this way it can add and remove people dynamically.

#Slack conversation API docs: 
#https://api.slack.com/docs/conversations-api
#Team channel and group Ids can be found when using slack on web
#ex: https://app.slack.com/client/T3JC5NEAG/G01LQJ2V73N/user_groups/S01LRK6B3DE
#T3JC5NEAG(teamId), G01LQJ2V73N(channelId), S01LRK6B3DE(groupId)

slack_token = 'xoxb-120413762356-1668984234166-EMhMSHzdEyuHDUXTnWmqwOnt'


def serviceNotification(msg):
    """Sends msg to Slack"""

    webhook_url = 'https://hooks.slack.com/services/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'
    slack_data = {'text': msg}

    response = requests.post(
    webhook_url, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

def errorNotification(serviceName, ex):
    """Sends an error msg to Slack using serviceName and error message"""

    msg = 'ERROR in ' + serviceName + '\n' + str(ex)
    webhook_url = 'https://hooks.slack.com/services/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'
    slack_data = {'text': msg}

    response = requests.post(
    webhook_url, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
     

class Slacker:
    def __init__(self):
        self.channelId = None
        self.serviceName = None
        self.logs = None
         
    

    def __create_private_channel_and_get_channelId(self, channelName):
        """Creates a private channel and returns the channelId\n
         channelName : string"""

        try:
            response = requests.post('https://slack.com/api/conversations.create', {
                'token': slack_token,
                'name': channelName,   
                'is_private': 'true'
            }).json()
            if response['ok']:
                return response['channel']['id']
            else:
                if self.logs:
                    self.logs.error(response['error'])
                print(response['error'])    

        except Exception as e:
            if self.logs:
                self.logs.error(e)
            print('Something went wrong in __create_private_channel_and_get_channelId')
            print(str(e))  

    def __get_user_private_channels(self, userId):
        """Returns all private channels for given userId\n
        userId : string"""
        try:
            response = requests.post('https://slack.com/api/users.conversations', {
                'token': slack_token, 
                'user': userId,
            'types': 'private_channel'
            }).json()
            if response['ok']:
                return response['channels']
            else:
                if self.logs:
                    self.logs.error(response['error'])
                print(response['error'])

        except Exception as e:
            if self.logs:
                self.logs.error(str(e))
            print('Something went wrong in __get_user_private_channels')
            print(str(e))

    def __get_group_userIds(self, groupId): 
        """Returns a comma separated string of userIds for a given groupId ex.'user1,user2,user3'\n
        group : string
        """

        try:
            response = requests.post('https://slack.com/api/usergroups.users.list', {
                'token': slack_token,
                'usergroup': groupId,
            }).json()
            print(response)
            if response['ok']:
                print("get user ids")
                userIds = response['users']
                separator = ','
                userIds = separator.join(userIds)
                return userIds
            else:
                if self.logs:
                    self.logs.error(response['error'])
                print(response['error'])    

        except Exception as e:
            if self.logs:
                self.logs.error(str(e))
            print('Something went wrong in __get_group_userIds')
            print(str(e))        


    def __invite_userIds_to_channelId(self, userIds, channelId):
        """Invites a comma separated string of userIds to join a channel by channelId\n
        userIds: string - comma separated userIds ex. 'W1234567890,W1234567440,W12654644'\n
        channelId : string - ex. 'C1234567890'"""

        try:
            response = requests.post('https://slack.com/api/conversations.invite', {
                'token': slack_token,
                'channel': channelId,
                'users': userIds    
            }).json()
            if response['ok'] == True:  
                return response
            else:
                if self.logs:
                    self.logs.error(response['error'])
                print(response['error'])    
        except Exception as e:
            if self.logs:
                self.logs.error(str(e))
            print('Something went wrong in invite_userId_to_channelId')
            print(str(e))                   


    def __get_bot_private_channels(self):
        """Returns all private bot channels"""

        userIdBot = 'U01KNUY6W4W'
        channels = self.__get_user_private_channels(userIdBot)
        return channels


    def __get_it_team_userIds(self): 
        """returns all itTeam userId's (comma separated string)"""

        itGroupId = 'S01LRK6B3DE'
        userIds = self.__get_group_userIds(itGroupId)
        return userIds


    def __get_channel_users(self, channelId):
        try:
            response = requests.post('https://slack.com/api/conversations.members', {
                'token': slack_token,
                'channel': channelId,    
            }).json()
            if response['ok'] == True:  
                return response
            else:
                if self.logs:
                    self.logs.error(response['error'])
                print(response['error'])    
        except Exception as e:
            if self.logs:
                self.logs.error(str(e))
            print('Something went wrong in get_channel_users')
            print(str(e))                   


    def __kick_user_from_channel(self, userId):
        try:
            response = requests.post('https://slack.com/api/conversations.kick', {
                'token': slack_token,
                'channel': self.channelId,  
                'user': userId,  
            }).json()
            if response['ok'] == True:  
                return response
            else:
                if self.logs:
                    self.logs.error(response['error'])
                print(response['error'])    
        except Exception as e:
            if self.logs:
                self.logs.error(str(e))
            print('Something went wrong in kick_user_from_channel')
            print(str(e))                    


    def __kick_non_channel_members(self):
        userIdBot = 'U01KNUY6W4W'

        itTeam = self.__get_it_team_userIds().split(',')
        channelUsers = self.__get_channel_users(self.channelId)['members']   

        for user in channelUsers:
            if user in itTeam or user == userIdBot :
                print(f"{user}, OK, you can stay") 
            else:
                print(f"{user}, No longer a member, Kick")  
                self.__kick_user_from_channel(user) 



    def setup(self, serviceName, logger = None):
        """Creates a channel if it does not yet exist\n
        invites all of the IT Team to that channel,\n
        sets the channelId so messages can be sent via the log function"""
        
        self.logs = logger
        self.serviceName = serviceName.lower()
        channelId = None
        print(self.serviceName)

        # 1. Get private channel - If channel doesn't exist create a new one.
        prefix = "error-"
        channels = self.__get_bot_private_channels()
        print(channels)
        if channels:
            for channel in channels:
                if (prefix + self.serviceName) == channel['name']:
                    print("channel already exists")
                    self.channelId = channel['id']
                    print("set channel ID to:" + self.channelId)
                    if self.logs:
                        self.logs.debug("Channel Id: " + self.channelId)
                    break

            else:
                print("Channel doesn't exist yet - creating new channel")
                channelId = self.__create_private_channel_and_get_channelId(prefix + self.serviceName)
                if channelId:
                    self.channelId = channelId
                    print("set channel ID to:" + self.channelId)
                    if self.logs:
                        self.logs.debug("Channel Id: " + self.channelId)
                            

            # 2 Invite IT-group to channel.
            if self.channelId: 
                userIds = self.__get_it_team_userIds()
                print(userIds)
                if userIds:
                    print(userIds)
                    response = self.__invite_userIds_to_channelId(userIds, self.channelId)
                    print(response)
                    if response:
                        if self.logs:
                            self.logs.debug('invite successful')
                            print('invite success')
                    else:
                        if self.logs:
                            self.logs.debug('Bad response - No invite')
                        print('Bad response - No invite') 
                else:
                    if self.logs:
                        self.logs.debug('Bad response - UserIds')
                    print('Bad response - UserIds: ' + userIds) 
            else:
                if self.logs:
                    self.logs.debug('No channelId')
                print('No channelId') 

            # 3 Kick non-group members:
            self.__kick_non_channel_members()
                


    def log(self, msg):
        """Send message to channel\n
        msg: string"""

        if self.channelId == None:
            if self.logs:
                self.logs.debug('must run setup first')
            print('must run setup first')

        else:
            try:
                response = requests.post('https://slack.com/api/chat.postMessage', {
                    'token': slack_token,
                    'channel': self.channelId,
                    'text': msg  
                }).json()
                if response['ok']:
                    return response
                else:
                    if self.logs:
                        self.logs.error(response['error'])
                    print(response['error'])    

            except Exception as e:
                if self.logs:
                    self.logs.error(str(e))
                print('Something went wrong')
                print(str(e))    




