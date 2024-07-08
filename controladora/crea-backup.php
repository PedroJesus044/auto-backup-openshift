<?php 

include "config.php";
  if (isset($_POST['submit'])) {
    $name = $_POST['name'];
    $sql = "INSERT INTO backup(id_backup, name) VALUES (null,'$name')";
    $result = $conn->query($sql);
    if ($result != TRUE) {
      echo "Error:". $sql . "<br>". $conn->error;
    }
    $conn->close(); 
  }

?>

<?php include 'assets/header.php';?>

<h2>Ingresa nuevo backup</h2>

<form action="" method="POST">

  <fieldset>

    <table style="width: 100%;">
        <tr>
            <th style="width: 25%;">Nombre del backup</th>
            <th style="width: 75%;"><input type="text" name="name"></th>
        </tr>
    </table>

    <br><br>

    <input type="submit" name="submit" value="submit" class="btn btn-primary">
    <a class="btn btn-success" href="view.php">Regresar</a>
  </fieldset>

</form>

<?php include 'assets/footer.php';?>
