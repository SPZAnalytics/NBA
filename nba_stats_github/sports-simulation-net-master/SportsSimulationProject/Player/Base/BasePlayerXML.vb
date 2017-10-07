Option Strict On

Imports System.IO
Imports System.Xml
Imports System.Xml.XPath

Namespace Player
    Namespace Base

        ''' <summary>
        ''' Expected XML structure
        ''' <code>
        ''' <Season year="2010">
        '''  <TeamSeason>
        '''    <Points>2010</Points>
        '''    <Rebounds>201</Rebounds>
        '''  </TeamSeason>
        '''  <TeamSeason>
        '''   <Points>2010</Points>
        '''    <Rebounds>201</Rebounds>
        '''  </TeamSeason>
        '''</Season>
        ''' </code>
        ''' </summary>
        Public Class BasePlayerXML

            ''' <summary>
            ''' Initializes a new instance of the <see cref="BasePlayerXML" /> class.
            ''' </summary>
            Public Sub New()

            End Sub

            ''' <summary>
            ''' Loads player's biographical data from XML file.
            ''' </summary>
            ''' <param name="fn">XML filename.</param>
            ''' <param name="id">Id attribute of player.</param>
            ''' <returns><see cref="BasePlayer"></see></returns>
            ''' <remarks>Makes strong assumptions about XML file structure, should validate against schema.</remarks>
            Public Function LoadBioFromXML(ByVal fn As String, ByVal id As String) As BasePlayer
                ' instantiate player object
                Dim player As BasePlayer = New BasePlayer
                ' get XML document from filename, throw exception if fails
                Dim doc As XmlDocument = Me.CreateXMLDocument(fn)
                ' use XPath to get player by ID
                Dim playerNode As XmlNode = GetPlayerNodeById(doc, id)
                ' get attribute list, throw exception if fails
                Dim atts As XmlAttributeCollection = GetAttributeList(playerNode)
                For Each att As XmlAttribute In atts
                    Me.AddPropertyFromAttribute(player, att)
                Next
                Return player
            End Function

            ''' <summary>
            ''' Loads player's biographical data from XML file.
            ''' </summary>
            ''' <param name="fn">XML filename.</param>
            ''' <param name="id">Id attribute value</param>
            ''' <returns><see cref="BasePlayer"></see></returns>
            ''' <remarks>Makes strong assumptions about XML file structure, should validate against schema.</remarks>
            Public Function LoadStatsFromXML(ByVal fn As String, ByVal id As String) As BasePlayer
                Dim player As New BasePlayer
                Dim doc As XmlDocument = Me.CreateXMLDocument(fn)
                Dim xpathQueryString As String = "//Player[@id='" & id & "']"
                Dim playerNode As XmlNode = GetPlayerNodeById(doc, id)
                Dim playerNodeSeasons As XmlNodeList = GetPlayerNodeSeasons(playerNode)
                For Each playerNodeSeason As XmlNode In playerNodeSeasons
                    Dim bps As New BasePlayerSeason
                    bps.Year = CInt(playerNodeSeason.Attributes("year").Value)
                    bps.AddPlayerTeamSeasons(Me.CreatePlayerTeamSeasonsFromSeasonNode(playerNodeSeason))
                    player.AddSeason(bps)
                Next
                Return player
            End Function

            'private methods
            
            ''' <summary>
            ''' Adds property to <see cref="BasePlayer"></see> from attribute.
            ''' </summary>
            ''' <param name="player"><see cref="BasePlayer"></see></param>
            ''' <param name="att"><see cref="XmlAttribute"></see></param>
            Private Sub AddPropertyFromAttribute(ByVal player As BasePlayer, ByVal att As XmlAttribute)
                Select Case att.Name
                    Case "FirstName"
                        Try
                            player.FirstName = att.Value
                        Catch
                            player.FirstName = Nothing
                        End Try
                    Case "MiddleName"
                        Try
                            player.MiddleName = att.Value
                        Catch
                            player.MiddleName = Nothing
                        End Try
                    Case "LastName"
                        Try
                            player.LastName = CStr(att.Value)
                        Catch
                            player.LastName = Nothing
                        End Try
                    Case "Suffix"
                        Try
                            player.Suffix = CStr(att.Value)
                        Catch
                            player.Suffix = Nothing
                        End Try
                    Case "BirthDate"
                        Try
                            player.BirthDate = CDate(att.Value)
                        Catch
                            player.BirthDate = Nothing
                        End Try
                    Case "Height"
                        Try
                            player.Height = CInt(att.Value)
                        Catch
                            player.Height = Nothing
                        End Try
                    Case "Weight"
                        Try
                            player.Weight = CInt(att.Value)
                        Catch
                            player.Weight = Nothing
                        End Try
                End Select
            End Sub

            ''' <summary>
            ''' Creates list of <see cref="BasePlayerTeamSeason"></see> from season node.
            ''' </summary>
            ''' <param name="seasonNode">The season node.</param>
            ''' <returns></returns>
            Private Function CreatePlayerTeamSeasonsFromSeasonNode(ByVal seasonNode As XmlNode) As List(Of BasePlayerTeamSeason)
                ' create new list of BasePlayerTeamSeason
                Dim lpts As New List(Of BasePlayerTeamSeason)
                Dim teamSeasonNodes As XmlNodeList = seasonNode.SelectNodes(".//TeamSeason")
                If teamSeasonNodes Is Nothing Then
                    Throw New Exception("No team seasons found in player season.")
                End If
                For Each teamSeason As XmlNode In teamSeasonNodes
                    Dim bts As New BasePlayerTeamSeason
                    Dim stats As Dictionary(Of String, Object) = Me.CreateTeamSeasonStats(teamSeason)
                    If stats Is Nothing Then
                        Throw New Exception("Stats dictionary cannot be empty")
                    End If
                    bts.Stats = stats
                    lpts.Add(bts)
                Next
                Return lpts
            End Function

            ''' <summary>
            ''' Creates the team season stats.
            ''' </summary>
            ''' <param name="teamSeason">XMLNode.</param>
            ''' <returns>Dictionary of statName and statValue.</returns>
            Private Function CreateTeamSeasonStats(ByVal teamSeason As XmlNode) As Dictionary(Of String, Object)
                Dim stats As New Dictionary(Of String, Object)
                For Each statElement As XmlElement In teamSeason.ChildNodes
                    If String.IsNullOrEmpty(statElement.Name) Or String.IsNullOrEmpty(statElement.InnerText) Then
                        Throw New Exception("Stat element name and value cannot be empty.")
                    End If
                    stats.Add(statElement.Name, statElement.InnerText)
                Next
                Return stats
            End Function

            ''' <summary>
            ''' Creates the XML document.
            ''' </summary>
            ''' <param name="fn">XMLFilename.</param>
            ''' <returns><see cref="XmlDocument"></see></returns>
            Private Function CreateXMLDocument(ByVal fn As String) As XmlDocument
                If Not File.Exists(fn) Then
                    Throw New Exception("Cannot load XML: " & fn.ToString & " does not exist")
                End If
                Dim doc As XmlDocument = New XmlDocument
                Try
                    doc.Load(fn)
                Catch ex As Exception
                    Console.WriteLine("Couldn't load XML file: " & fn)
                End Try
                Return doc
            End Function

            ''' <summary>
            ''' Gets the attribute list as XmlAttributeCollection.
            ''' </summary>
            ''' <param name="playerNode">XmlNode representing player.</param>
            ''' <returns>List of attributes.</returns>
            Private Function GetAttributeList(ByVal playerNode As XmlNode) As XmlAttributeCollection
                Dim atts As XmlAttributeCollection = playerNode.Attributes
                If atts Is Nothing Then
                    Throw New Exception("Attribute collection is empty.")
                End If
                Return atts
            End Function

            ''' <summary>
            ''' Uses XPath query to find player by id value.
            ''' </summary>
            ''' <param name="doc"><see cref="XmlDocument"></see></param>
            ''' <param name="id">Id string.</param>
            ''' <returns><see cref="XmlNode"></see></returns>
            Private Function GetPlayerNodeById(ByVal doc As XmlDocument, ByVal id As String) As XmlNode
                Dim xpathQueryString As String = "//Player[@id='" & id & "']"
                Dim playerNode As XmlNode = doc.SelectNodes(xpathQueryString)(0)
                If playerNode Is Nothing Then
                    Throw New Exception("Document has no player nodes.")
                End If
                Return playerNode
            End Function

            ''' <summary>
            ''' Gets XmlNodeList representing list of seasons.
            ''' </summary>
            ''' <param name="playerNode">XmlNode.</param>
            ''' <returns>XmlNodeList representing seasons.</returns>
            Private Function GetPlayerNodeSeasons(ByVal playerNode As XmlNode) As XmlNodeList
                Dim seasons As XmlNodeList = playerNode.SelectNodes(".//Season")
                If seasons Is Nothing Or seasons.Count = 0 Then
                    Throw New Exception("Player node has no seasons.")
                End If
                Return seasons
            End Function

        End Class
    End Namespace
End Namespace

