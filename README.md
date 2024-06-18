# SQL Data Access

This project simplifies working with SQLite and Postgres databases by providing essential functions for creating, reading, and managing databases and tables. It allows for easy data insertion and retrieval. There are two versions of SQlite access,
SQLiteDataAccess use logger extension to log errors, the SQLiteDataAccessExtLog allow you to ask if error occures and so, it is possible to store it another ways.

## Features

- Create database 
- Retrieve table and column names
- Create tables with specified columns
- Insert data into tables
- Retrieve data from tables
- Delete tables

## Version
 - 2.0: Changed the insert method. Instead of adding data as a list of dictionaries in separate columns, data is now added as a list of rows. This allows for inserting more rows in one step. Keep in mind that all insertions need to have the same column types.

## License

**Copyright 2024, kisb-data **  
kisbalazs.data@gmail.com 

## License

This code is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This code is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this code. If not, see <http://www.gnu.org/licenses/>.

## Warranty Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---