

Configuration in :file:`~/metapack.yaml`. It's best to create a user with
limited permissions, such as a role of Editor.

.. code-block:: yaml


    wordpress:
        example:
            url: https://example.com/xmlrpc.php
            user: metauser
            password: 9t&password*fU
        othersite:
            url: https://otehrsite.com/xmlrpc.php
            user: metapack
            password: LO7^K#QpasswordWvgjRLIW


Errors
------


"CRITICAL: User metapack does not have permissions to add terms to taxonomies."
Users with roles less than Editor can't create tags and categories. change the
role to 'Editor' or ensure that the tags and categories already exist.