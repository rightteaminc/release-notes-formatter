**Deployed By:** [Pete Soderberg](mailto:pete@getparallax.com)

**Work Items**


- [9176](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=9176) - Create new Pagination Model in the Public API Project



- [9569](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=9569) - Public Clients Endpoints returning 500 responses



- [9395](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=9395) - BE Work (Enhance Active Projects CSV Download)



- [9370](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=9370) - Pipeline CSV upload allows project name changes



- [9574](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=9574) - Created and Modified dates not accurate on public GET Client



- [9137](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=9137) - Update Client Endpoint



- [9151](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=9151) - Manage Pipelines via CRM API

- [9227](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=9227) - Add Paginated Command Handlers for Client List

- [9575](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=9575) - Max and Min length errors on create client Name length displays property as "{PropertyName}"



- [9468](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=9468) - CRM sync - allow unbounded Client Annual Revenue



- [9588](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=9588) - PATCH to Update Client returning error that Name must be a string, even if it is



- [9612](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=9612) - GET /v/1clients with no parameters returns a page and page_size of 0



- [8947](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=8947) - People import returns 409 error when attempting to upload a file with a new person that has an email already in use.



- [9232](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=9232) - Add endpoint template



- [9570](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=9570) - PTO Upload Units are case sensitive



- [9556](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=9556) - Revisit NetSuite date converter to solve for issue between MM/DD/YYYY and DD/MM/YYYY



- [9417](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=9417) - Expiration Date set to day after entered date





- [9402](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=9402) - PXTS: More records in submission summary table than timesheet summary table









- [9616](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=9616) - Success Response returned if an empty name is sent in



- [9156](https://dev.azure.com/parallax-app/Parallax/_workitems?_a=edit&id=9156) - List Pipelines Endpoint





**Pull Requests**









- [81b9e15a482ca2bc5154599c86413d9861e508fa](https://github.com/rightteaminc/parallax-server/commit/81b9e15a482ca2bc5154599c86413d9861e508fa) - AB#9176 Adds PagedResults model for Public API









- [03119aea08a8a8bd9a0e2ca9584ca632d680e52c](https://github.com/rightteaminc/parallax-server/commit/03119aea08a8a8bd9a0e2ca9584ca632d680e52c) - AB#9569 Fix 500 Error on client API calls





















- [ee83564172a8fff949b1f64e3d4e61c3523c33a7](https://github.com/rightteaminc/parallax-server/commit/ee83564172a8fff949b1f64e3d4e61c3523c33a7) - AB#9395 Active project CSV export detail









- [bc336f8414261b382cad00d199b4d160e7f2c80d](https://github.com/rightteaminc/parallax-server/commit/bc336f8414261b382cad00d199b4d160e7f2c80d) - AB#9370 - Updates CSV import to prevent certain name changes











- [b536aee5748b8ff247f9279db9329e59d3059170](https://github.com/rightteaminc/parallax-server/commit/b536aee5748b8ff247f9279db9329e59d3059170) - AB#9574 Fix Created, Modified and IsArchived fields for client



















- [d03f2cb3e865037f7c175014495204281979b6c5](https://github.com/rightteaminc/parallax-server/commit/d03f2cb3e865037f7c175014495204281979b6c5) - AB#9137 Update Client Public API IsArchived







- [523fa3806925ca193d9cf3003047acc7c8613a76](https://github.com/rightteaminc/parallax-server/commit/523fa3806925ca193d9cf3003047acc7c8613a76) - Adding IsArchived bool to the contract for Get Clients endpoint







- [44a4dcf2fd0c7a9e42902dd9105b55364dd2076a](https://github.com/rightteaminc/parallax-server/commit/44a4dcf2fd0c7a9e42902dd9105b55364dd2076a) - AB#9468 - Adds support for annual revenue changes in client projection













- [0b61d252f1b6133b673be331b2f79501bd79a337](https://github.com/rightteaminc/parallax-server/commit/0b61d252f1b6133b673be331b2f79501bd79a337) - AB#9588 Possible Validator fixes







- [f25af8a8c0fcc8770c433dd33b383a085350fb37](https://github.com/rightteaminc/parallax-server/commit/f25af8a8c0fcc8770c433dd33b383a085350fb37) - AB#9612 Fixes obvious issue with page and page size mapping to the PagedResult







- [9276da35e5b3fe173177eaf8f3a935b9ae5e4148](https://github.com/rightteaminc/parallax-server/commit/9276da35e5b3fe173177eaf8f3a935b9ae5e4148) - AB#8947 Employee csv import full fail on dupe email













- [d9b232339335d204de55dbf5c113524523014a9b](https://github.com/rightteaminc/parallax-server/commit/d9b232339335d204de55dbf5c113524523014a9b) - AB#9232 adding operation filters for our swagger docs to endpoints









- [3c188f590f1c1a274e503f7ce485aa8ec1249048](https://github.com/rightteaminc/parallax-server/commit/3c188f590f1c1a274e503f7ce485aa8ec1249048) - AB#9570 Change bamboo pto upload unit validation to case insensitive







- [995f72c1c88b2a0a72cc109e91b334cb545454ca](https://github.com/rightteaminc/parallax-server/commit/995f72c1c88b2a0a72cc109e91b334cb545454ca) - AB#9556 Updating Netsuite plugin











- [bc3762afdd9aa4b79230d039aec2bd0f63911728](https://github.com/rightteaminc/parallax-server/commit/bc3762afdd9aa4b79230d039aec2bd0f63911728) - AB#9417 Changes expiration calculation







- [bb3b0f34b7750906a19892c56babd8a2bd13d61d](https://github.com/rightteaminc/parallax-server/commit/bb3b0f34b7750906a19892c56babd8a2bd13d61d) - Revert "Revise the JobQueueingFilter to only skip when enqueued"











- [e1fc847750956dcd2698ede2bdb642848b835654](https://github.com/rightteaminc/parallax-server/commit/e1fc847750956dcd2698ede2bdb642848b835654) - AB#9402 decouple offering connect and sync (project merge PR 1)



















- [2b2d558f37dc6688f871743c173dba284dd61722](https://github.com/rightteaminc/parallax-server/commit/2b2d558f37dc6688f871743c173dba284dd61722) - AB#9402 Move efforts and actuals move/merge logic to a job (project merge PR 2)













- [bee2699ea8c7d5bbe2a3343042d9f2127bed6c37](https://github.com/rightteaminc/parallax-server/commit/bee2699ea8c7d5bbe2a3343042d9f2127bed6c37) - AB#9402 Update submissions in batches during project merge (project merge PR 3)







- [e87c13b6eec982e97a0705239f70bb59cb616a2c](https://github.com/rightteaminc/parallax-server/commit/e87c13b6eec982e97a0705239f70bb59cb616a2c) - Updates CRM Client import to ignore problematic annual revenue values







- [e6bf8483b89534b14d403674f285b31beed42321](https://github.com/rightteaminc/parallax-server/commit/e6bf8483b89534b14d403674f285b31beed42321) - AB#9616 Fixes name validator issue with updating



























- [68a007f62a48512a5ba99e1d42afe2297ee49f9c](https://github.com/rightteaminc/parallax-server/commit/68a007f62a48512a5ba99e1d42afe2297ee49f9c) - AB#9156 List pipeline endpoint for Public API







- [a74df2c91bf2e16a25fbf56cb318032dec8207d2](https://github.com/rightteaminc/parallax-server/commit/a74df2c91bf2e16a25fbf56cb318032dec8207d2) - Try to get Octopus deployments to fail faster when facing "too many requests" error



