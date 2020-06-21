const ConfirmDelete = () => {
  var x = confirm("Are you sure you want to delete?");
  if (x)
      return true;
  else
    return false;
}
const ConfirmDeleteRecording = () => {
  var x = confirm("Are you sure you want to delete this recording? This can not be undone!");
  if (x)
      return true;
  else
    return false;
}