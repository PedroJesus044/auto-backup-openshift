<?php 

include "config.php"; 

if (isset($_GET['id'])) {

    $id_backup = $_GET['id'];

    $sql = "DELETE FROM backup WHERE id_backup=$id_backup";

     $result = $conn->query($sql);

     if ($result == TRUE) {

        header('Location: view.php');

    }else{

        echo "Error:" . $sql . "<br>" . $conn->error;

    }

} 

?>