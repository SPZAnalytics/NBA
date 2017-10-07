Option Strict On

Imports SportsSimulation.Player.Base
Imports SportsSimulation.Team.Base
Imports System.Linq

Namespace League
    Namespace Base
        ' need to test new Get methods, also update class diagram 2010-08-02 16:48
        ''' <summary>
        ''' 	BaseLeague
        ''' 	----------
        ''' 	+Id: String
        ''' 	+Players: List(of BasePlayer)
        ''' 	+StatCategories: List(of String)
        ''' 	+Teams: List(of BaseTeam)
        ''' 	----------
        '''     +AddPlayer (player: BasePlayer)
        '''     +AddPlayers (players: List(of BasePlayer))
        ''' 	+AddTeam (team: BaseTeam)
        ''' 	+AddTeams (teams: List(of BaseTeam))
        '''     +GetLeaguePlayerAverageByStat (players: List(of BasePlayer), statName: String): Double
        '''     +GetLeaguePlayerPerTimePeriodByStat (players: List(of BasePlayer), statName: String): Double
        '''     +GetLeagueTeamAverageByStat (players: List(of BasePlayer), statName: String): Double
        '''     +GetLeagueTeamPerTimePeriodByStat (players: List(of BasePlayer), statName: String): Double
        '''     +GetLeagueTotalByStat (players: List(of BasePlayer), statName: String): Double
        ''' 	+GetTeam (teams: List(of BaseTeam), idToMatch: String): BaseTeam
        ''' 	+GetTeams (teams: List(of BaseTeam), idsToMatch: List(of String): List(of BaseTeam)	
        ''' </summary>
        Public Class BaseLeague

			''' <summary>
            ''' Gets or sets the league id.
            ''' </summary>
            ''' <value>The league's id.</value>
            Public Property Id As String
            ''' <summary>
            ''' Gets or sets list of players.
            ''' </summary>
            ''' <value><see cref="List(of BasePlayer)"></see></value>
            Public Property Players() As List(Of BasePlayer)
            ''' <summary>
            ''' Need list of stat categories to perform team aggregate calculations.
            ''' </summary>
            ''' <value>List of stat categories.</value>
            Public Property StatCategories As List(Of String)
			''' <summary>
            ''' Gets or sets list of teams.
            ''' </summary>
            ''' <value><see cref="List(of BaseTeam)"></see></value>
            Public Property Teams() As List(Of BaseTeam)
            ''' <summary>
            ''' Gets or sets the year.
            ''' </summary>
            ''' <value>The league year.</value>
            Public Property Year() As Integer
            
            ' public methods
            ''' <summary>
            ''' Initializes a new instance of the <see cref="BaseLeague" /> class.
            ''' </summary>
            Public Sub New()
                Me.Players = New List(Of BasePlayer)
				Me.StatCategories = New List(Of String)
				Me.Teams = New List(Of BaseTeam)
            End Sub

            ''' <summary>
            ''' Initializes a new instance of the <see cref="BaseTeam" /> class.
            ''' </summary>
            ''' <param name="statCategories">List of stat categories.</param>
            ''' <remarks>Chose flexible implementation where can choose what stats matter. If need rigid list, 
            ''' then can subclass and use constant instead of permitting assignment when creating object.</remarks>
            Public Sub New(ByVal statCategories As List(Of String))
                Me.Players = New List(Of BasePlayer)
                Me.StatCategories = statCategories
				Me.Teams = New List(Of BaseTeam)
            End Sub

            ''' <summary>
            ''' Adds player to list of players.
            ''' </summary>
            ''' <param name="player"><see cref="BasePlayer"></see></param>
            Public Sub AddPlayer(ByVal player As BasePlayer)
                Me.Players.Add(player)
            End Sub

            ''' <summary>
            ''' Adds list of players to existing list of players.
            ''' </summary>
            ''' <param name="players"><see cref="List(of BasePlayer)"></see></param>
            Public Sub AddPlayers(ByVal players As List(Of BasePlayer))
                For Each bp As BasePlayer In players
                    Me.AddPlayer(bp)
                Next
            End Sub

            ''' <summary>
            ''' Adds team to list of teams.
            ''' </summary>
            ''' <param name="team"><see cref="BaseTeam"></see></param>
            Public Sub AddTeam(ByVal team As BaseTeam)
                Me.Teams.Add(team)
            End Sub

            ''' <summary>
            ''' Adds list of teams to existing list of teams.
            ''' </summary>
            ''' <param name="teams"><see cref="List(of BaseTeam)"></see></param>
            Public Sub AddTeams(ByVal teams As List(Of BaseTeam))
                For Each bt As BaseTeam In teams
                    Me.AddTeam(bt)
                Next
            End Sub

            ' TO ADD
            '     +GetLeagueTeamPerTimePeriodByStat (players: List(of BasePlayer), statName: String): Double
            '     +GetLeagueTotalByStat (players: List(of BasePlayer), statName: String): Double

            Public Function GetLeaguePlayerAverageByStat(ByVal players As List(Of BasePlayer), ByVal statName As String, ByVal year As Integer) As Double
                If players.Count = 0 Then
                    Throw New Exception("Must have at least one player to calculate aggregate stat.")
                End If
                Dim tot As Double = Me.GetLeaguePlayerTotalByStat(players, statName, year)
                Return tot / players.Count
            End Function

            Public Function GetLeaguePlayerTimePeriodByStat(ByVal players As List(Of BasePlayer), ByVal statName As String, ByVal year As Integer, ByVal timePeriod As Integer) As Double
                If players.Count = 0 Then
                    Throw New Exception("Must have at least one player to calculate aggregate stat.")
                End If
                If timePeriod = 0 Or timePeriod < 48 Then
                    Throw New Exception("Must have time period greater than zero and no more than 48.")
                End If
                Dim tot As Double = Me.GetLeaguePlayerTotalByStat(players, statName, year)
                Dim mins As Double = Me.GetLeaguePlayerTotalByStat(players, "Minutes", year)
                If mins = 0 Then
                    Throw New Exception("Minutes cannot be zero. Must have at least one minute played to calculate aggregate stat.")
                End If
                Return tot / mins * timePeriod
            End Function

            Public Function GetLeaguePlayerTotalByStat(ByVal players As List(Of BasePlayer), ByVal statName As String, ByVal year As Integer) As Double
                Dim tot As Double = 0
                If players.Count = 0 Then
                    Throw New Exception("Must have at least one player to calculate aggregate stat.")
                End If
                For Each bp As BasePlayer In players
                    Dim stat As Double = bp.GetSeasonTotal(statName, year)
                    If stat = Nothing Then
                        Throw New Exception("Season total cannot be nothing")
                    End If
                    tot += stat
                Next
                Return tot
            End Function

            Public Function GetLeagueTeamPerTimePeriodByStat(ByVal teams As List(Of BaseTeam), ByVal statName As String, ByVal timePeriod As Integer) As Double
                If Teams.Count = 0 Then
                    Throw New Exception("Must have at least one team to calculate aggregate stat.")
                End If
                If timePeriod = 0 Or timePeriod < 48 Then
                    Throw New Exception("Must have time period greater than zero and no more than 48.")
                End If
                Dim tot As Double = Me.GetLeagueTeamTotalByStat(teams, statName, Year)
                Dim mins As Double = Me.GetLeagueTeamTotalByStat(teams, "Minutes", Year)
                If mins = 0 Then
                    Throw New Exception("Minutes cannot be zero. Must have at least one minute played to calculate aggregate stat.")
                End If
                Return tot / mins * timePeriod
            End Function

            Public Function GetLeagueTeamTotalByStat(ByVal teams As List(Of BaseTeam), ByVal statName As String, ByVal year As Integer) As Double
                Dim tot As Double = 0
                If teams.Count = 0 Then
                    Throw New Exception("Must have at least one team to calculate aggregate stat.")
                End If
                For Each bt As BaseTeam In teams
                    Dim stat As Double = bt.TeamStatTotal(bt.Players, statName, year)
                    If stat = Nothing Then
                        Throw New Exception("Season total cannot be nothing")
                    End If
                    tot += stat
                Next
                Return tot
            End Function

            ''' <summary>
            ''' Gets the team by teamid.
            ''' </summary>
            ''' <param name="teams">List of teams to search.</param>
            ''' <param name="idToMatch">The id to match.</param>
            ''' <returns>If match, <see cref="BaseTeam"></see>; otherwise, Nothing.</returns>
            Public Function GetTeam(ByVal teams As List(Of BaseTeam), ByVal idToMatch As String) As BaseTeam
                For Each team As BaseTeam In teams
                    If team.Id = idToMatch Then
                        Return team
                    End If
                Next
                Return Nothing
            End Function

            ''' <summary>
            ''' Gets list of teams from a list of team ids.
            ''' </summary>
            ''' <param name="teams">List of teams to search.</param>
            ''' <param name="idsToMatch">The ids to match.</param>
            ''' <returns>If match, <see cref="List(of BaseTeam)"></see>; otherwise, Nothing.</returns>
            Public Function GetTeams(ByVal teams As List(Of BaseTeam), ByVal idsToMatch As String) As List(Of BaseTeam)
                Dim teamsMatchIds As New List(Of BaseTeam)
                For Each id As String In idsToMatch
                    Dim team As BaseTeam = Me.GetTeam(teams, id)
                    If Not team Is Nothing Then
                        teamsMatchIds.Add(team)
                    End If
                Next
                Return teamsMatchIds
            End Function

        End Class
    End Namespace
End Namespace