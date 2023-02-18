# scheduling_system
scheduling system project
Django application using Django graphene that can be connected to PostgreSQL the application is for scheduling system that allows the user to create a reservable timing that others can book using it. 

# Step to setup Project
 1. git clone https://github.com/dipakgupta12/scheduling_system.git
 2. Install python and create a virtual environment 
      $ command: virtualenv -p python 3.6 "your environment name"
 3. Activate you environment
      $ command: source "your environment"/bin/activate/
 4. Change your current directory to project directory
 5. Install all requirements of this project 
      $ command: pip install -r requirements.txt
 6. Migrate models with your db
      $ commands: python manage.py makemigrations 
                  python manage.py migrate  
 7. Run your server
      $ command: Python manage.py runserver
 8. For localhost the url is : http://127.0.0.1:8000/dashboard/

# Here are the some  django graphene query and mutation
1.query to get all scheduling meeting
<br/>
```query{ 
  allScheduleMeeting
   {
    id
    isBooked
    fromMeetingDateTime
    toMeetingDateTime
    userName
    userEmail
    meetingTimeInterval
    meetingCreator {
      id
      username
    }
  }
}
```
2.query to get all scheduling meeting of respective user
<br/>
```query{ 
  allSchedulingMeetingOfUser(meetingCreator:"utkarsh")
   {
    id
    isBooked
    fromMeetingDateTime
    toMeetingDateTime
    userName
    userEmail
    meetingTimeInterval
    meetingCreator {
      id
      username
    }
  }
}
```
3.query to get all scheduling meeting of current user
<br/>
```query{ 
  allSchedulingMeetingOfOwner
   {
    id
    isBooked
    fromMeetingDateTime
    toMeetingDateTime
    userName
    userEmail
    meetingTimeInterval
    meetingCreator {
      id
      username
    }
  }
}
```
4.query to get single scheduling meeting 
<br/>
```query{
  scheduleMeeting(id:id){
    meetingCreator{
      id
      username
    }
    id
    isBooked
    fromMeetingDateTime
    toMeetingDateTime
    meetingTimeInterval
  }
}
```
5.dummy response 
```{
  "data": {
    "allSchedulingMeetingOfUser": [
      {
        "id": "68",
        "isBooked": false,
        "fromMeetingDateTime": "2021-12-31T17:43:00+00:00",
        "toMeetingDateTime": "2021-12-31T18:13:00+00:00",
        "userName": null,
        "userEmail": null,
        "meetingTimeInterval": "A_30_MIN",
        "meetingCreator": [
          {
            "id": "2",
            "username": "utkarsh"
          }
        ]
      },
      {
        "id": "69",
        "isBooked": false,
        "fromMeetingDateTime": "2021-12-30T17:46:00+00:00",
        "toMeetingDateTime": "2021-12-30T18:01:00+00:00",
        "userName": null,
        "userEmail": null,
        "meetingTimeInterval": "A_15_MIN",
        "meetingCreator": [
          {
            "id": "2",
            "username": "utkarsh"
          }
        ]
      }
    ]
  }
}
```
6.Mutation to create a schedule meeting 
 ```
 #########################################################Mutations########################################################      
 mutation{
  createMeeting(fromMeetingDateTime:"2023-12-30T17:46:00+00:00" meetingTimeInterval: "15 MIN")
      {
        meeting {
          id
          isBooked
          userName
          userEmail
          fromMeetingDateTime
          meetingTimeInterval
        }
      }
      }
#########################################################Response########################################################      
{
  "data": {
    "createMeeting": {
      "meeting": {
        "id": "70",
        "isBooked": false,
        "userName": null,
        "userEmail": null,
        "fromMeetingDateTime": "2023-12-30T17:46:00+00:00",
        "meetingTimeInterval": "A_15_MIN"
      }
    }
  }
}
```
7.Mutation to update a schedule meeting 
```
 #########################################################Mutations########################################################      
 mutation{
  updateMeeting(id:70 fromMeetingDateTime:"2024-12-30T17:46:00+00:00" meetingTimeInterval: "15 MIN")
      {
        meeting {
          id
          isBooked
          userName
          userEmail
          fromMeetingDateTime
          meetingTimeInterval
        }
      }
      }#########################################################Response########################################################      
{
  "data": {
    "createMeeting": {
      "meeting": {
        "id": "70",
        "isBooked": false,
        "userName": null,
        "userEmail": null,
        "fromMeetingDateTime": "2023-12-30T17:46:00+00:00",
        "meetingTimeInterval": "A_15_MIN"
      }
    }
  }
}
```
8.Mutation to book you slot of  meeting 
```
 #########################################################Mutations########################################################      
 mutation{
  updateMeeting(id:70  userName:"xyz" userEmail:"xyz@gmail.com")
      {
        meeting {
          id
          isBooked
          userName
          userEmail
          fromMeetingDateTime
          meetingTimeInterval
        }
      }
      }#########################################################Response########################################################      
{
  "data": {
    "createMeeting": {
      "meeting": {
        "id": "70",
        "isBooked": false,
        "userName": "xyz",
        "userEmail": "xyz@gmail.com",
        "fromMeetingDateTime": "2023-12-30T17:46:00+00:00",
        "meetingTimeInterval": "A_15_MIN"
      }
    }
  }
}
```
9.Mutation to delete a scheduling meeting 

```mutation{
  deleteMeeting(id:70){
        meeting {
          id
          isBooked
          userName
          userEmail
          fromMeetingDateTime
          meetingTimeInterval
        }
      }
      }```
