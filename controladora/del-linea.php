<?php 

include "config.php"; 

if (isset($_GET['id_codigo'])) {

    $id_codigo = $_GET['id_codigo'];
    $id_backup = $_GET['id_backup'];

    $sql = "DELETE FROM codigo WHERE id_codigo='$id_codigo'";

     $result = $conn->query($sql);

     if ($result == TRUE) {
        header('Location: view-codigo.php?id='.$id_backup);
        echo "Record deleted successfully.";
    }else{

        echo "Error:" . $sql . "<br>" . $conn->error;

    }

} 

?>