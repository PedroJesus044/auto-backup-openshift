<?php include 'assets/header.php';?>
<?php
include "config.php";
    if (isset($_GET['id'])) {
        $id_backup = $_GET['id'];
        $sql = "SELECT COUNT(*) as cant_bloques from (SELECT * from codigo where id_backup=".$id_backup." group by no_bloque) cant_bloques";
        
        $result = $conn->query($sql);
                if ($result->num_rows > 0) {
                    $row = $result->fetch_assoc();
                    $cant_bloques = $row['cant_bloques'];
                }
    }
?>
<?php
$sql = 'SELECT no_bloque from codigo where id_backup = '.$_GET['id'].' group by no_bloque order by no_bloque';
$result = $conn->query($sql);
while ($row = $result->fetch_assoc()) {
    $sql = "SELECT id_codigo, no_bloque, no_linea, linea FROM codigo WHERE id_backup=".$id_backup." AND no_bloque=".$row['no_bloque']." ORDER BY no_linea";
    $result2 = $conn->query($sql);
    echo '<div class="m-4 border">';
    echo "<h3>Bloque: ".$row['no_bloque']."</h3>";
        while($row2 = $result2->fetch_assoc()){
            echo '<div>'.$row2['no_linea'].' - '.htmlentities($row2['linea']).'<a type="button" href="del-linea.php?id_codigo='.$row2['id_codigo'].'&id_backup='.$_GET['id'].'" class="btn btn-danger" style="float: right;">Borrar</a><a type="button" href="edit-linea.php?id_codigo='.$row2['id_codigo'].'" class="btn btn-primary" style="float: right;">Editar</a></div><br>';
        }
    echo '<a class="btn btn-success" href="add-linea.php?id_backup='.$_GET['id'].'&id_bloque='.$row['no_bloque'].'">Nueva línea</a>';
    echo "</div>";
}

?>

<br>
<div class="m-4">
    <a class="btn btn-info" href="add-bloque.php?id_backup=<?php echo $_GET['id']; ?>">Nuevo bloque</a>
    <a class="btn btn-success" href="view.php">Regresar</a>
</div>
<?php include 'assets/footer.php';?>