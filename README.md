# strava-aws-serveless

## What
Strava API client over aws serverless components

## Why

Test and explore serverless capabilities and show how to securely interact with a third party which authorizes users with OAuth.

## How

In order to create an API client for Strava there are some bootstrapping steps that need to happen first. The most important is registering an app over Strava which will create a set of credentials that will identify said app going forward. Also while doing so, there is need to have a backend to respond to strava in a certain way for authorization and for activities incoming from Strava.

Strava API Values and Credentials must be stored in a secure manner but still made available only to required parts of the system. These vales are a client id, a client secret; also while registering an app the Credentials for current user that is registering the app and they are a pair of tokens one for access with expiration of 6 hours and a refresh token that does not expire. This is slightly confusing as there are credentials for an app and credentials for each authenticated user or Athlete. Meaning there should be pairs of credentials per each user which approves this appliation plus the application itself. Also interesting for this is that every time an access token has expired, it must be refreshed with an api call that will respond with the new access token and a new refresh token.

Also per API Terms applications must implement a web hook that can handle deauthorizations, new activities, changes in visibility of activities and also to avoid hitting rate limits.


```mermaid
C4Context
      title System Context diagram for Strava API Client
      Enterprise_Boundary(b0, "API Project Boundary") {
        Person(admin, "Admin")

          System_Boundary(b1, "AWS Serverless API Client") {
            System_Boundary(b3, "Admin Plane") {
              System(credentialsHandler, "App Credentials handler")
              System(stravaHook, "Strava Hook API Gateway")
              
              SystemDb(CredentialsDb, "Credentials Storage")
              System(hookHandler, "Hook Handler")
            }
        }
        System_Boundary(b2, "Strava API System") {
          System(stravaApi, "Strava API")
        }
      }
      Rel(credentialsHandler, CredentialsDb, "Uses", "HTTPS")
      Rel(credentialsHandler, stravaApi, "Uses", "sync JSon/HTTPS")
      Rel(stravaApi, stravaHook, "Uses", "sync/async, JSon/HTTPS")
      Rel(stravaHook, hookHandler, "Uses", "sync invocation")
      Rel(admin, credentialsHandler, "Uses", "https")
      UpdateLayoutConfig($c4ShapeInRow="4", $c4BoundaryInRow="2")

```



```mermaid
C4Context
      title System Context diagram for Strava API Client
      Enterprise_Boundary(b0, "API Project Boundary") {
        Person(athlete, "Athlete")  
        Person(admin, "Admin")

          System_Boundary(b1, "AWS Serverless API Client") {
            System(athleteAPI, "API Athlete")
            System_Boundary(b3, "Admin Plane") {
              System(credentialsHandler, "App Credentials handler")
              System(stravaHook, "API Hook Gateway")
              
              SystemDb(CredentialsDb, "Credentials Storage")
              System(hookHandler, "Hook 1")
            }
            
            
            System(activitiesHandler, "Activities handler")
            
            SystemDb(ActivitiesDb, "Activities")
        }
        System_Boundary(b2, "Strava API System") {
          System(stravaApi, "Strava API")
        }
      }
      Rel(credentialsHandler, CredentialsDb, "Uses", "HTTPS")
      Rel(credentialsHandler, stravaApi, "Uses", "sync JSon/HTTPS")
      Rel(stravaApi, stravaHook, "Uses", "sync/async, JSon/HTTPS")
      Rel(stravaHook, hookHandler, "Uses", "sync invocation")
      Rel(admin, CredentialsDb, "Stores", "Bootstrap")
      Rel(athlete, athleteAPI, "Uses", "sync Json/HTTPS")
      Rel(athleteAPI, activitiesHandler, "Uses", "sync invocation")
      Rel(activitiesHandler, ActivitiesDb, "Uses", "sync")
      Rel(activitiesHandler, stravaApi, "Uses", "sync JSon/HTTPS")

      UpdateLayoutConfig($c4ShapeInRow="4", $c4BoundaryInRow="2")

```
