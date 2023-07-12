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
        }
        Boundary(b5, "API"){
          System(stravaHook, "Strava Hook API Gateway")
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

## Functionality concept map

Once there is an authenticated app there are muliple ways to query for information but for this integration I'll be using only Athletes and SummaryActivities. Given that the credentials (tokens) for the default user are already provided upon registration we can start some designs in that regards but the design will be made to support multiple Athletes from the start.

Given that the models for Athlete and Activities are different and have different conceptually they are modeled as distinct boundaries but as the interaction with Strava API is mostly the same the similar parts will also be separated to a gatherer boundary that can also interact with credentials boundary and no other part of the system besides the admin should interact with it.

```mermaid
C4Context
  title System Context diagram for Strava API Client v2
  Enterprise_Boundary(b0, "API Project Boundary") {
    Person(athlete, "Athlete")
    Person(admin, "Admin")

      System_Boundary(b1, "AWS Serverless API Client") {
        System(athleteUI, "Athlete UI")
        Boundary(aws, "AWS Cloud"){
          System(athleteAPI, "Athlete API")
          Boundary(backend, "Backend"){

            System(hookHandler, "Hook Handler")
            Boundary(b4, "Activity Plane") {
              System(athleteHandler, "Athlete Handler")
              System(athleteGatherer, "Athlete gatherer")
              SystemDb(athleteDb, "Athletes Storage")
            }
            Boundary(b6, "Acrivity Plane"){
              System(activityHandler, "Activity Handler")
              System(activityGatherer, "Activity gatherer")
              SystemDb(activityDb, "Activities Storage")

            }
            Boundary(b7, "Gathering"){

              System(gatherer, "Gatherer")
              SystemQueue(q1,"q1")
            }
            Boundary(b3, "Admin Plane") {
              System(credentialsHandler, "App Credentials Handler")
              SystemDb(credentialsDb, "Credentials Storage")
            }
            
          }
        }
    }
    System_Boundary(b2, "Strava API System") {
      System(stravaWeb, "Strava Web")
      System(stravaApi, "Strava API")
    }
  }
  Rel(athlete, stravaWeb, "Uses","https")
  Rel(athlete, athleteUI, "Uses","https")

  Rel(athleteUI, athleteAPI, "Uses", "https")

  Rel(athleteAPI, athleteHandler, "Uses", "https")
  Rel(athleteAPI, activityHandler, "Uses", "https")
  
  Rel(credentialsHandler, credentialsDb, "Uses", "HTTPS")
  Rel(credentialsHandler, stravaApi, "Uses", "sync JSon/HTTPS")
  Rel(athleteGatherer, gatherer, "Uses", "sync JSon/HTTPS")
  Rel(activityGatherer, gatherer, "Uses", "sync JSon/HTTPS")
  Rel(gatherer, q1, "Writes", "Events Athletes/Activities")
  Rel(athleteGatherer, q1, "Reads")
  Rel(activityGatherer, q1, "Reads")


  Rel(stravaApi, athleteAPI, "Uses", "sync/async, JSon/HTTPS")
  Rel_D(athleteAPI, hookHandler, "Uses", "sync invocation")
  Rel(hookHandler, activityHandler, "Uses", "sync invocation")

  Rel(hookHandler, athleteHandler, "Uses", "sync invocation")
  Rel(hookHandler, credentialsHandler, "Uses", "sync invocation")
  Rel(admin, credentialsHandler, "Uses", "https")

  Rel(athleteHandler, athleteDb, "Reads", "https")
  Rel_L(activityHandler, activityDb, "Reads", "https")
  Rel(athleteGatherer, athleteDb, "Writes", "https")
  Rel_L(activityGatherer, activityDb, "Writes", "https")
  Rel(gatherer, credentialsHandler, "Uses", "https")
  Rel(gatherer, stravaApi, "Uses", "https")


  UpdateLayoutConfig($c4ShapeInRow="5", $c4BoundaryInRow="5")

```

[License](LICENSE.md)