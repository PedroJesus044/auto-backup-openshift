<?php include 'assets/header.php';?>
<?php 

include "config.php";

    if (isset($_POST['submit'])) {
        $id_codigo = $_GET['id_codigo'];

        $no_bloque = $_POST['no_bloque'];

        $no_linea = $_POST['no_linea'];

        $linea = $_POST['linea'];

        $id_backup = $_POST['id_backup'];

        if(isset($_POST['run_as_sudo'])) $run_as_sudo = 1;
        else $run_as_sudo = 0;
    
        if(isset($_POST['paralelo'])) $paralelo = 1;
        else $paralelo = 0;

        $sql = 'UPDATE codigo SET no_bloque="'.$no_bloque.'", no_linea="'.$no_linea.'", linea="'.$linea.'", run_as_sudo='.$run_as_sudo.', paralelo='.$paralelo.' WHERE id_codigo='.$id_codigo; 

        $result = $conn->query($sql); 

        if ($result == TRUE) {

        }else{
            echo "Error:" . $sql . "<br>" . $conn->error;
        }

    } 

if (isset($_GET['id_codigo'])) {

    $id_codigo = $_GET['id_codigo'];

    $sql = "SELECT * FROM codigo WHERE id_codigo=".$id_codigo;

    $result = $conn->query($sql);

    if ($result->num_rows > 0) {        

        while ($row = $result->fetch_assoc()) {

            $no_bloque = $row['no_bloque'];

            $no_linea = $row['no_linea'];

            $linea = $row['linea'];

            $id_backup = $row['id_backup'];

            if($row['run_as_sudo']==true) $run_as_sudo  = 'checked';
            else $run_as_sudo  = '';

            if($row['paralelo']==true) $paralelo  = 'checked';
            else $paralelo  = '';

        } 

    ?>

<form action="" method="POST">

  <fieldset>

    <input type="hidden" name="id_backup" value="<?php echo $id_backup;?>"><br>


    <table style="width: 100%;">
        <tr>
            <th style="width: 25%;">Número de bloque</th>
            <th style="width: 75%;"><input type="number" name="no_bloque" value=<?php echo $no_bloque;?> style="width: 100%;"></th>
        </tr>
        <tr>
            <th style="width: 25%;">Número de línea</th>
            <th style="width: 75%;"><input type="number" name="no_linea" value=<?php echo $no_linea;?> style="width: 100%;"></th>
        </tr>
        <tr>
            <th style="width: 25%;">Línea de código a ejecutar</th>
            <th style="width: 75%;"><input type="text" name="linea" value="<?php echo htmlentities($linea);?>" style="width: 100%;"></th>
        </tr>
        <tr>
            <th style="width: 25%;">Ejecutar como sudo</th>
            <th style="width: 75%;"><input type="checkbox" name="run_as_sudo" <?php echo $run_as_sudo;?>></th>
        </tr>
        <tr>
            <th style="width: 25%;">Ejecutar en paralelo</th>
            <th style="width: 75%;"><input type="checkbox" name="paralelo" <?php echo $paralelo;?>></th>
        </tr>
    </table>

    <br><br>

    <input type="submit" class="btn btn-primary" name="submit" value="Actualizar">
    <a class="btn btn-success" href="view-codigo.php?id=<?php echo $id_backup; ?>">Regresar</a>

  </fieldset>

</form>

    <?php

    } else{ 

        header('Location: view.php');

    } 

}

?> 
<?php include 'assets/footer.php';?>