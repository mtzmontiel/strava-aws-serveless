# strava-aws-serveless
Strava API client over aws serverless components

In order to create an API client for Strava there are some bootstrapping steps that need to happen first. The most important is registering an app over Strava which will create a set of credentials that will identify said app going forward. Also while doing so, there is need to have a backend to respond to strava in a certain way.


```mermaid
C4Context
      title System Context diagram for Strava API Client
      Enterprise_Boundary(b0, "API Project Boundary") {
        Person(admin, "Admin")

          System_Boundary(b1, "AWS Serverless API Client") {
            System_Boundary(b3, "Admin Plane") {
              System(credentialsHandler, "App Credentials handler")
              System(stravaHook, "Authorization Hook Gateway")
              
              SystemDb(CredentialsDb, "Credentials Storage")
              System(hookHandler, "Hook 1")
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
...

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
