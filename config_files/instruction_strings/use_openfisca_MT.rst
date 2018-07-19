==========================================================================================
Instruction to use Openfisca Managing Tool
==========================================================================================

Hello there, thanks for installing openfisca Managing Tool!
In this document, we will see how to use the three main functionalities of this software:

- The legislationExplorer_;
- The reformMaker_;
- The simulationMaker_;

.. _legislationExplorer:

************************************************************************************
Legislation Explorer
************************************************************************************

This feature allow to see what's inside an **openfisca-country system**.

.. image:: img/openfisca_system/openfisca_instruction/visualize_TBS/openfisca_choose_VTBS.png
   :height: 300px
   :width: 600 px
   :scale: 50 %

Once you've clicked the button you could select between three groups:

- The **Variables**;
- The **Parameters**;
- The **Reforms**.

After chose a group, on the left you could choose a set of files and directories that contains openfisca structures of the chosen type.
You can choose any file within the set and see all the data structures that contains on the right of the windows (the waiting time depends on the number of structures within file).

.. image:: img/openfisca_system/openfisca_instruction/visualize_TBS/visualize_OFS.png
   :height: 300px
   :width: 600 px
   :scale: 50 %

**N.B.** You can't select a **directory**, you can select only a file within it. To navigate between files contained in a directory, click on the arrow at the left of the directory name.

.. image:: img/openfisca_system/openfisca_instruction/visualize_TBS/navigate_directory.png
   :height: 300px
   :width: 600 px
   :scale: 50 %

.. _reformMaker:

************************************************************************************
Reform Maker
************************************************************************************

This feature allow to create an **openfisca-reform**.

.. image:: img/openfisca_system/openfisca_instruction/reform_maker/openfisca_choose_MR.png
   :height: 300px
   :width: 600 px
   :scale: 50 %

Once you've clicked the button you could select between three reforms type:

- The addVariable_;
- The updateVariable_;
- The neutralizeVariable_;
- The other options are not available.


.. image:: img/openfisca_system/openfisca_instruction/reform_maker/all_reforms.png
   :height: 300px
   :width: 600 px
   :scale: 50 %


.. _addVariable:

Add variable
====================================================================================
If you wish to add a variable, you must select the option "**Add Variable**" in the reforms menù. Next, you can name
the reform and add a description to it.

Note that the first two fields are disabled, you could use those when you'll decide to **Update a variable**.

.. image:: img/openfisca_system/openfisca_instruction/reform_maker/add_variable1.png
   :height: 300px
   :width: 600 px
   :scale: 50 %

However, you can decide to avoid the naming of the reform or/and to insert a description for it: the system will provide a standard naming.
Next you can choose to turn back home or goes to specify the fields of the new variable.

.. image:: img/openfisca_system/openfisca_instruction/reform_maker/add_variable2.png
   :height: 300px
   :width: 600 px
   :scale: 50 %

As you can see in the image above, you can specify all the fields typical of an Openfisca variable.
To make sure that the reform will be created, you must specify the necessary fields to define a variable which are:

- The **name**;
- The **entity**;
- The **type**;
- The **period**.

Of course you can specify the other fields too. Once you've finish you can select the **Run operation** button and see
the generated reform in legislationExplorer_.

.. _updateVariable:

Update variable
====================================================================================
If you wish to update a variable, you must select the option "**Update Variable**" in the reforms menù.
Next, you can name the reform and add a description to it.

Note that the first two fields are enabled because you have to select an **existing variable** to update it.
For sure, you can't modify a variable that doesn't exist!

.. image:: img/openfisca_system/openfisca_instruction/reform_maker/up_variable1.png
   :height: 300px
   :width: 600 px
   :scale: 50 %

However, you can decide to avoid the naming of the reform or/and to insert a description for it: the system will provide a standard naming.
Next you can choose to turn back home or goes to modify the fields of the selected variable.

.. image:: img/openfisca_system/openfisca_instruction/reform_maker/up_variable2.png
   :height: 300px
   :width: 600 px
   :scale: 50 %

As you can see in the image above, when you decide to update a variable, all the current information of that Openfisca variable
are displayed.

To make sure that the reform will be created, you must modify at least one field except the name (which is unchangeable).

Of course you can modify from one to n fields. Once you've finish you can select the **Run operation** button and see
the generated reform in legislationExplorer_.

.. _neutralizeVariable:

Neutralize variable
====================================================================================


.. _simulationMaker:

************************************************************************************
Simulation Maker
************************************************************************************
aldo