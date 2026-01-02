/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstlast.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/13 00:56:10 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/30 20:58:31 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
// #include <stdio.h>
// #include <stdlib.h>

t_list	*ft_lstlast(t_list *lst)
{
	if (!lst)
		return (NULL);
	while (lst->next)
		lst = lst->next;
	return (lst);
}

// int	main(void)
// {
// 	t_list	*head = NULL;
// 	t_list	*last;
// 	int		v1 = 1, v2 = 2, v3 = 3;

// 	ft_lstadd_front(&head, ft_lstnew(&v1));
// 	ft_lstadd_front(&head, ft_lstnew(&v2));

// 	last = ft_lstlast(head);
// 	if (last)
// 	printf("Last node content: %d (Expected: 1)\n", *(int *)(last->content));
// 	else
// 		printf("List is empty.\n");
// }