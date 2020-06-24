const ConfirmDelete = () => {
  var x = confirm("Are you sure you want to delete?");
  if (x)
      return true;
  else
    return false;
}
const ConfirmDeleteComposition = () => {
  var x = confirm("Are you sure you want to delete this composition? Clicking OK will delete the composition and all of the attached relationships including recordings information. This cannot be undone.");
  if (x)
      return true;
  else
    return false;
}
const ConfirmDeleteWriter = () => {
  var x = confirm("Are you sure you want to delete this writer? All of the attached relationships to any compositions will also be lost. This cannot be undone.");
  if (x)
      return true;
  else
    return false;
}
const ConfirmDeletePublishingCompany = () => {
  var x = confirm("Are you sure you want to delete this publishing company? All of the attached relationships to any compositions will also be lost. This cannot be undone.");
  if (x)
      return true;
  else
    return false;
}
const ConfirmDeleteRecording = () => {
  var x = confirm("Are you sure you want to delete? This can not be undone!");
  if (x)
      return true;
  else
    return false;
}