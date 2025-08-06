# Detailed Explanation of all the views
 

## class ListView(generics.ListAPIView):
A view that list all the books in the Library
  
   
## class DetailView(generics.RetrieveAPIView):
A  view that retrieve all  the details if a particular book

    
## class CreateView(generics.CreateAPIView):

A View that handles the creation of a book instance by an authenticated user



## class UpdateView(generics.UpdateAPIView):
A view that Handles The Update of book instances


## class DeleteView(generics.DestroyAPIView):
A view that handle the deletion of a book instance
by an authenticated user