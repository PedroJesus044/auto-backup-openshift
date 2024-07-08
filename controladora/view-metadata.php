<?php include 'assets/header.php';?>
<div class="m-4 border">
<?php
$creado = FALSE;
include "config.php";
    if (isset($_GET['id'])) {
        $id_backup = $_GET['id'];
        $sql = "SELECT * from metadata WHERE id_backup=".$id_backup;
        
        $result = $conn->query($sql);
                if ($result->num_rows > 0) {
                    $row = $result->fetch_assoc();

                    $id_backup = $row['id_backup'];
                    $ruta_respaldo = $row['ruta_respaldo'];
                    #$fecha = $row['fecha'];
                    $ip_servidor = $row['ip_servidor'];
                    $ip_nas = $row['ip_nas'];
                    #$id_metadata = null;
                    $rash = $row['rash'];
                    $pw_servidor = $row['pw_servidor'];
                    $user_servidor = $row['user_servidor'];
                    $port = $row['port'];
                    $reintentos_maximos = $row['reintentos_maximos'];
                    echo "<h2>Modifica la metadata del respaldo</h2>";
                    $creado = TRUE;
                }
                else{
                    echo "<h2>Por favor, ingresa la metadata del respaldo</h2>";
                    $id_backup = $_GET['id'];
                    $ruta_respaldo = '';
                    #$fecha = $row['fecha'];
                    $ip_servidor = '';
                    $ip_nas = '';
                    #$id_metadata = null;
                    $rash = 'echo <password> | sudo -S ';
                    $pw_servidor = '';
                    $user_servidor = '';
                    $port = null;
                    $reintentos_maximos = null;
                }
    }

    if (isset($_POST['crear'])) {
        $id_backup = $_POST['id_backup'];
        $ruta_respaldo = $_POST['ruta_respaldo'];
        $ip_servidor = $_POST['ip_servidor'];
        $ip_nas = $_POST['ip_nas'];
        $rash = $_POST['rash'];
        $port = $_POST['port'];
        $reintentos_maximos = $_POST['reintentos_maximos'];
        $user_servidor = $_POST['user_servidor'];
        $pw_servidor = $_POST['pw_servidor'];


        $sql = "INSERT INTO metadata (id_backup, ruta_respaldo, ip_servidor, ip_nas, id_metadata, rash, port, reintentos_maximos, user_servidor, pw_servidor) values (".$id_backup.", '".$ruta_respaldo."','".$ip_servidor."', '".$ip_nas."', null, '".$rash."', ".$port.", ".$reintentos_maximos.", '".$user_servidor."', '".$pw_servidor."')";

        $result = $conn->query($sql);
        if ($result != TRUE) {
        echo "Error:". $sql . "<br>". $conn->error;
        }
    }

    if (isset($_POST['actualizar'])) {
        $id_backup = $_POST['id_backup'];
        $ruta_respaldo = $_POST['ruta_respaldo'];
        $ip_servidor = $_POST['ip_servidor'];
        $ip_nas = $_POST['ip_nas'];
        $rash = $_POST['rash'];
        $port = $_POST['port'];
        $reintentos_maximos = $_POST['reintentos_maximos'];
        $user_servidor = $_POST['user_servidor'];
        $pw_servidor = $_POST['pw_servidor'];


        $sql = "UPDATE metadata SET ruta_respaldo='".$ruta_respaldo."', ip_servidor='".$ip_servidor."', ip_nas='".$ip_nas."', rash='".$rash."', port=".$port.", reintentos_maximos=".$reintentos_maximos.", user_servidor='".$user_servidor."', pw_servidor='".$pw_servidor."' where id_backup = ".$id_backup;

        $result = $conn->query($sql);
        if ($result != TRUE) {
        echo "Error:". $sql . "<br>". $conn->error;
        }
    }
?>



<form action="" method="POST">

  <fieldset>

    <table style="width: 100%;">
    <tr>
        <th style="width: 25%;">Metadata perteneciente al backup</th>
        <th style="width: 75%;"><input type="number" name="id_backup" value=<?php echo $id_backup;?> style="width: 100%;"></th>
    </tr>

    <tr style="width: 100%;">
        <th style="width: 25%;">El respaldo se debe guardar en la siguiente ruta</th>
        <th style="width: 75%;"><input type="text" name="ruta_respaldo" value="<?php echo $ruta_respaldo;?>" style="width: 100%;"></th>
    </tr>

    <tr>
        <th style="width: 25%;">La IP del servidor a respaldar</th>
        <th style="width: 75%;"><input type="text" name="ip_servidor" value="<?php echo $ip_servidor;?>" style="width: 100%;" required></th>
    </tr>

    <tr>
        <th style="width: 25%;">El usuario del servidor a respaldar</th>
        <th style="width: 75%;"><input type="text" name="user_servidor" value="<?php echo $user_servidor;?>" style="width: 100%;" required></th>
    </tr>

    <tr>
        <th style="width: 25%;">La password del servidor a respaldar</th>
        <th style="width: 75%;"><input type="text" name="pw_servidor" value="<?php echo $pw_servidor;?>" style="width: 100%;" required></th>
    </tr>

    <tr>
        <th style="width: 25%;">La IP del nas donde se alojará el respaldo</th>
        <th style="width: 75%;"><input type="text" name="ip_nas" value="<?php echo $ip_nas;?>" style="width: 100%;"></th>
    </tr>

    <tr>
        <th style="width: 25%;">La cadena Run As Sudo Header (RASH)</th>
        <th style="width: 75%;"><input type="text" name="rash" value="<?php echo $rash;?>" style="width: 100%;" required></th>
    </tr>
    
    <tr>
        <th style="width: 25%;">El puerto SSH del servidor</th>
        <th style="width: 75%;"><input type="number" name="port" value=<?php echo $port;?> style="width: 100%;" required></th>
    </tr>

    <tr>
        <th style="width: 25%;">El número de reintentos</th>
        <th style="width: 75%;"><input type="number" name="reintentos_maximos" value=<?php echo $reintentos_maximos;?> style="width: 100%;" required></th>
    </tr>
    </table> 

    <br><br>

    <?php
        if($creado){
            ?><input type="submit" name="actualizar" value="Actualizar" class="btn btn-primary"><?php
        }else{
            ?><input type="submit" name="crear" value="Crear" class="btn btn-primary"><?php
        }
    ?>
    <a class="btn btn-success" href="view.php">Regresar</a>

  </fieldset>

</form>
</div>

<?php include 'assets/footer.php';?>