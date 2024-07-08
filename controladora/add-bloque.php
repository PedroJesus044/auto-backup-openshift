<?php include 'assets/header.php';?>
<?php
include "config.php";

if(isset($_GET['id_backup'])){
    $sql = 'SELECT COUNT(*) as cant_bloques from (SELECT * from codigo where id_backup='.$_GET['id_backup'].' group by no_bloque) cant_bloques';
    $result = $conn->query($sql);
    $row = $result->fetch_assoc();
    $cant_bloques = $row['cant_bloques'];
    $no_bloque = $cant_bloques + 1;
}

if (isset($_POST['submit'])) {
    $id_backup = $_GET['id_backup'];
    
    $no_linea = $_POST['no_linea'];
    $linea = $_POST['linea'];
    if(isset($_POST['run_as_sudo'])) $run_as_sudo = 1;
    else $run_as_sudo = 0;

    if(isset($_POST['paralelo'])) $paralelo = 1;
    else $paralelo = 0;

    $sql = "INSERT INTO codigo (id_codigo, id_backup, no_bloque, no_linea, linea, run_as_sudo, paralelo) values (null, ".$id_backup.", ".$no_bloque.", ".$no_linea.", '".$linea."', ".$run_as_sudo.", ".$paralelo.")";
    
    $result = $conn->query($sql);
    if ($result != TRUE) {
      echo "Error:". $sql . "<br>". $conn->error;
    }
    $conn->close(); 
}
?>

<h2>Ingresa nuevo bloque</h2>

<form action="" method="POST">

  <fieldset>

    <table style="width: 100%;">
        <tr>
            <th style="width: 25%;">Número de línea</th>
            <th style="width: 75%;"><input type="number" name="no_linea" value="1" style="width: 100%;"></th>
        </tr>
        <tr>
            <th style="width: 25%;">Línea de código a ejecutar</th>
            <th style="width: 75%;"><input type="text" name="linea" style="width: 100%;"></th>
        </tr>
        <tr>
            <th style="width: 25%;">Ejecutar como sudo</th>
            <th style="width: 75%;"><input type="checkbox" name="run_as_sudo"></th>
        </tr>
        <tr>
            <th style="width: 25%;">Ejecutar en paralelo</th>
            <th style="width: 75%;"><input type="checkbox" name="paralelo"></th>
        </tr>
    </table>

    <br><br>

    <input type="submit" name="submit" value="submit" class="btn btn-primary">
    <a class="btn btn-success" href="view-codigo.php?id=<?php echo $_GET['id_backup']; ?>">Regresar</a>

  </fieldset>

</form>


<?php include 'assets/footer.php';?>