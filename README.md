# Assessment
Assessment task for Saif Inspirations

1. I Implement JWT and tested it via Post man
   url is domain/api/token/
   {
    "username": "admin",
    "password": "admin"
}
 
   ![image](https://github.com/aijazmahdavi/assessment/assets/135382053/ab54d2fa-35d5-4726-a7ca-20587adf11a6)


2 and 3. Create Project and Task models and manage CRUD for users.
For testing this I made models and user I didnt make custom template for login or sign up as its not part of assements
> Model : Porject
> model: task

CRUD for selected user in premission will auto managed and tested it
1.super user username: admin password: admin
2.user1 = username: demouser password: Stranger@5
3.user2 = username: demouser1 password: Stranger@5


> if go to admin panel project via admin user then the person we assigned that project to can add task and CRUD these tasks
![image](https://github.com/aijazmahdavi/assessment/assets/135382053/4f7a5ad8-3b53-4400-ab35-745d78480837)

3.1 added permission handling for crud specify crud for user and manage who can only view or view and delete and udpate etc.
![Uploading image.png…]()


I added two users and assigned project to them they can manage crud thier tasks 

4. softdelete
   I applied softdelet funcitonality but I didnt create custom template for I added is deleted which can be used in template if user deletes entry.


![image](https://github.com/aijazmahdavi/assessment/assets/135382053/801902e7-0127-4f00-9b50-93f3991b8183)

