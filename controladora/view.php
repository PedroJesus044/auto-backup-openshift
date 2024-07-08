<?php 

include "config.php";

$sql = "SELECT * FROM backup";

$result = $conn->query($sql);

?>
<?php include 'assets/header.php';?>
    <div class="container">

        <h2>Backups</h2>

<table class="table">

    <thead>

        <tr>

        <th>ID</th>

        <th>Name</th>

        <th>Action</th>

    </tr>

    </thead>

    <tbody> 

        <?php

            if ($result->num_rows > 0) {

                while ($row = $result->fetch_assoc()) {

        ?>
                    <tr>

                    <td><?php echo $row['id_backup']; ?></td>

                    <td><?php echo $row['name']; ?></td>

                    <td>
                    <a role="button" class="btn btn-success" href="http://<?php echo $_ENV["ABKP_PY_HOST"];?>:<?php echo $_ENV["ABKP_PY_PORT"];?>?id=<?php echo $row['id_backup']; ?>">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-play" viewBox="0 0 16 16">
                        <path d="M10.804 8 5 4.633v6.734zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696z"></path>
                        </svg>
                    </a>    
                    &nbsp;<a class="btn btn-primary" href="view-codigo.php?id=<?php echo $row['id_backup']; ?>">Ver código</a>&nbsp;<a class="btn btn-primary" href="view-metadata.php?id=<?php echo $row['id_backup']; ?>">Ver metadata</a>&nbsp;<a class="btn btn-danger" href="del-backup.php?id=<?php echo $row['id_backup']; ?>">Delete</a></td>

                    </tr>                       

        <?php       }

            }

        ?>                

    </tbody>

</table>

<?php include 'assets/footer.php';?>

